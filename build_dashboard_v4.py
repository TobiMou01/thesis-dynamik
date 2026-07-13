#!/usr/bin/env python3
"""
Build Dashboard v4 – Dynamik-Explorer
Masterarbeit Tobias Mourier, TH Wildau

Liest alle CSV-Ergebnisse aus output/ und erzeugt eine einzige
self-contained HTML-Datei: output/dynamik_explorer.html

Einzige externe Abhängigkeit im Dashboard: Plotly.js (CDN)
"""
import json, csv, os, sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent / "output"

# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────
def read_csv(relpath):
    p = BASE / relpath
    if not p.exists():
        print(f"  WARN: {p} not found, skipping")
        return []
    with open(p, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def float_or_none(v):
    try: return round(float(v), 6)
    except: return None

def float4(v):
    try: return round(float(v), 4)
    except: return None

RATIOS = ["ROA","ROE","EBIT_margin","fcf_margin","current_ratio","debt_to_equity","equity_ratio"]
RATIO_LABELS = {"ROA":"ROA","ROE":"ROE","EBIT_margin":"EBIT-Marge","fcf_margin":"FCF-Marge",
                "current_ratio":"Current Ratio","debt_to_equity":"D/E Ratio","equity_ratio":"EK-Quote"}
RAW_COLS = ["netIncome","totalAssets","totalStockholderEquity","ebit","totalRevenue",
            "freeCashFlow","totalCurrentAssets","totalCurrentLiabilities","shortLongTermDebtTotal"]
RAW_LABELS = {"netIncome":"Net Income","totalAssets":"Total Assets","totalStockholderEquity":"Eigenkapital",
              "ebit":"EBIT","totalRevenue":"Umsatz","freeCashFlow":"Free Cash Flow",
              "totalCurrentAssets":"Umlaufvermögen","totalCurrentLiabilities":"Kurzfr. Verbindl.",
              "shortLongTermDebtTotal":"Schulden gesamt"}

print("=== Building Dashboard v4 Data ===")

# ─────────────────────────────────────────────
# 1) STATIC: ar_features + company profiles → per-ticker per-ratio data
# ─────────────────────────────────────────────
print("Loading static data...")
ar_rows = read_csv("ar/ar_features.csv")
profile_rows = read_csv("profiles/company_quadrant_profiles.csv")

# Build profile lookup
profiles = {}
for r in profile_rows:
    profiles[r["ticker"]] = r

# Load company names from raw profile CSVs
print("Loading company names from raw profiles...")
RAW_PROFILES_DIR = Path(__file__).parent / "data" / "raw" / "profiles"
company_names = {}  # ticker -> name
if RAW_PROFILES_DIR.exists():
    for fn in RAW_PROFILES_DIR.iterdir():
        if fn.suffix == '.csv':
            try:
                with open(fn, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    row = next(reader, None)
                    if row and 'symbol' in row and 'name' in row:
                        company_names[row['symbol']] = row['name']
            except:
                pass
print(f"  {len(company_names)} company names loaded")

# Build companies dict
companies = {}
for row in ar_rows:
    tk = row["ticker"]
    ratio = row["ratio"]
    if tk not in companies:
        pr = profiles.get(tk, {})
        companies[tk] = {
            "name": company_names.get(tk, tk),
            "sector": pr.get("sector",""),
            "industry": pr.get("industry",""),
            "market_cap": float_or_none(pr.get("market_cap","")),
            "employees": float_or_none(pr.get("employees","")),
            "dominant": pr.get("dominant_quadrant",""),
            "consistency": float4(pr.get("consistency_score","")),
            "quadrants": {},
            "phi1": {},
            "sigma": {},
            "phi1_se": {},
            "r2": {},
            "half_life": {},
            "kmeans": None
        }
    companies[tk]["phi1"][ratio] = float4(row.get("phi1",""))
    companies[tk]["sigma"][ratio] = float4(row.get("sigma_diff",""))
    companies[tk]["phi1_se"][ratio] = float4(row.get("phi1_se",""))
    companies[tk]["r2"][ratio] = float4(row.get("r_squared",""))
    companies[tk]["half_life"][ratio] = float4(row.get("half_life",""))

# Add quadrant assignments
qa_rows = read_csv("clustering/quadrant_assignments.csv")
for row in qa_rows:
    tk = row["ticker"]
    ratio = row["ratio"]
    if tk in companies:
        companies[tk]["quadrants"][ratio] = row.get("quadrant","")

# Add kmeans labels
km_rows = read_csv("clustering/kmeans_ar_dynamics_labels.csv")
for row in km_rows:
    tk = row["ticker"]
    if tk in companies:
        companies[tk]["kmeans"] = int(float(row.get("kmeans_ar_dynamics","0")))

static = {
    "ratios": RATIOS,
    "ratio_labels": RATIO_LABELS,
    "companies": companies
}

print(f"  {len(companies)} companies loaded")

# ─────────────────────────────────────────────
# 2) LEVELS: ratio_panel.csv → {ticker: {ratio: {quarters:[], values:[]}}}
# ─────────────────────────────────────────────
print("Loading levels data...")
levels = defaultdict(lambda: defaultdict(lambda: {"quarters":[],"values":[]}))
panel_rows = read_csv("ratios/ratio_panel.csv")
for row in panel_rows:
    tk = row["ticker"]
    q = row["quarter"]
    for ratio in RATIOS:
        v = float_or_none(row.get(ratio,""))
        if v is not None:
            levels[tk][ratio]["quarters"].append(q)
            levels[tk][ratio]["values"].append(v)

# Convert to regular dict for JSON
levels_dict = {tk: dict(ratios) for tk, ratios in levels.items()}
print(f"  {len(levels_dict)} tickers with level data")

# ─────────────────────────────────────────────
# 3) RAW: raw_values_panel.csv
# ─────────────────────────────────────────────
print("Loading raw data...")
raw_ts = defaultdict(lambda: defaultdict(lambda: {"quarters":[],"values":[]}))
raw_rows = read_csv("ratios/raw_values_panel.csv")
for row in raw_rows:
    tk = row["ticker"]
    q = row["quarter"]
    for col in RAW_COLS:
        v = float_or_none(row.get(col,""))
        if v is not None:
            raw_ts[tk][col]["quarters"].append(q)
            raw_ts[tk][col]["values"].append(v)

raw_dict = {tk: dict(cols) for tk, cols in raw_ts.items()}
print(f"  {len(raw_dict)} tickers with raw data")

# ─────────────────────────────────────────────
# 4) INTERDEPENDENCE
# ─────────────────────────────────────────────
print("Loading interdependence data...")

def read_matrix(relpath):
    rows = read_csv(relpath)
    if not rows: return {"labels":RATIOS,"matrix":[]}
    labels = [r for r in RATIOS if r in rows[0]]
    mat = []
    for row in rows:
        mat.append([float4(row.get(r,"")) for r in labels])
    return {"labels": labels, "matrix": mat}

phi1_corr = read_matrix("interdependence/corr_phi1.csv")
sigma_corr = read_matrix("interdependence/corr_sigma.csv")
pval_phi1 = read_matrix("interdependence/pval_phi1.csv")
pval_sigma = read_matrix("interdependence/pval_sigma.csv")

# Cramér's V crosstabs
crosstab_rows = read_csv("interdependence/quadrant_crosstabs.csv")
cramers = []
for row in crosstab_rows:
    cramers.append({
        "ratio_a": row["ratio_a"],
        "ratio_b": row["ratio_b"],
        "cramers_v": float4(row.get("cramers_v","")),
        "chi2": float4(row.get("chi2","")),
        "p": float_or_none(row.get("chi2_pval",""))
    })

interdependence = {
    "phi1_corr": phi1_corr,
    "sigma_corr": sigma_corr,
    "pval_phi1": pval_phi1,
    "pval_sigma": pval_sigma,
    "cramers": cramers
}

# ─────────────────────────────────────────────
# 5) VALIDATION (FF3)
# ─────────────────────────────────────────────
print("Loading validation data...")

chi2_rows = read_csv("profiles/ff3_chi2_results.csv")
chi2 = []
for row in chi2_rows:
    chi2.append({
        "ratio": row["ratio"],
        "chi2": float4(row.get("chi2","")),
        "p_value": float_or_none(row.get("p_value","")),
        "cramers_v": float4(row.get("cramers_v","")),
        "n_tickers": int(float(row.get("n_tickers","0"))),
        "significant": row.get("significant","") == "True"
    })

size_rows = read_csv("profiles/ff3_size_effects.csv")
size_effects = []
for row in size_rows:
    size_effects.append({
        "ratio": row["ratio"],
        "size_var": row["size_variable"],
        "target": row["target"],
        "rho": float4(row.get("spearman_rho","")),
        "p": float_or_none(row.get("p_value","")),
        "significant": row.get("significant","") == "True"
    })

consistency_rows = read_csv("profiles/consistency_summary.csv")
consistency = {}
for row in consistency_rows:
    consistency[row["metric"]] = {
        "mean": float4(row.get("mean","")),
        "median": float4(row.get("median","")),
        "std": float4(row.get("std","")),
        "pct_fully": float4(row.get("pct_fully_consistent","")),
        "pct_majority": float4(row.get("pct_majority",""))
    }

# Company consistency scores for histogram
company_consistency = []
for tk, pr in sorted(profiles.items()):
    sc = float4(pr.get("consistency_score",""))
    if sc is not None:
        company_consistency.append({
            "ticker": tk,
            "score": sc,
            "dominant": pr.get("dominant_quadrant",""),
            "sector": pr.get("sector","")
        })

validation = {
    "chi2": chi2,
    "size_effects": size_effects,
    "consistency": consistency,
    "company_consistency": company_consistency
}

# ─────────────────────────────────────────────
# 6) CLUSTERING
# ─────────────────────────────────────────────
print("Loading clustering data...")

diag_rows = read_csv("clustering/kmeans_ar_dynamics_diagnostics.csv")
km_diagnostics = [{"k": int(float(r["k"])), "silhouette": float4(r["silhouette"]), "inertia": float4(r["inertia"])} for r in diag_rows]

thresh_rows = read_csv("clustering/quadrant_thresholds.csv")
thresholds = {r["ratio"]: {"phi1_med": float4(r["phi1_median"]), "sigma_med": float4(r["sigma_median"])} for r in thresh_rows}

summary_rows = read_csv("clustering/quadrant_summary.csv")
quadrant_summary = []
for r in summary_rows:
    quadrant_summary.append({
        "ratio": r["ratio"],
        "KS": int(float(r.get("KORREKTIV-STABIL","0"))),
        "KV": int(float(r.get("KORREKTIV-VOLATIL","0"))),
        "PS": int(float(r.get("PERSISTENT-STABIL","0"))),
        "PV": int(float(r.get("PERSISTENT-VOLATIL","0")))
    })

clustering = {
    "diagnostics": km_diagnostics,
    "thresholds": thresholds,
    "quadrant_summary": quadrant_summary
}

# ─────────────────────────────────────────────
# 7) ROBUSTNESS
# ─────────────────────────────────────────────
print("Loading robustness data...")

sample_comp_rows = read_csv("robustness/sample_comparison.csv")
sample_comparison = []
for r in sample_comp_rows:
    sample_comparison.append({
        "sample": r["sample"],
        "min_q": int(float(r.get("min_quarters","0"))),
        "ratio": r["ratio"],
        "n": int(float(r.get("n","0"))),
        "phi1_median": float4(r.get("phi1_median","")),
        "sigma_median": float4(r.get("sigma_median","")),
        "signif_pct": float4(r.get("signif_pct",""))
    })

ticker_counts = read_csv("robustness/sample_ticker_counts.csv")
sample_counts = [{"sample": r["sample"], "min_q": int(float(r.get("min_quarters","0"))),
                  "n_tickers": int(float(r.get("n_tickers","0")))} for r in ticker_counts]

# Financial services comparison - aggregate medians per ratio per sample
fs_rows = read_csv("robustness/financial_services.csv")
fs_data = defaultdict(lambda: defaultdict(list))
for r in fs_rows:
    sample = r.get("sample","")
    ratio = r.get("ratio","")
    phi1 = float_or_none(r.get("phi1",""))
    if phi1 is not None:
        fs_data[sample][ratio].append(phi1)

# Compute medians
import statistics
fs_medians = {}
for sample, ratios in fs_data.items():
    fs_medians[sample] = {}
    for ratio, vals in ratios.items():
        vals.sort()
        fs_medians[sample][ratio] = round(statistics.median(vals), 4)

robustness = {
    "sample_comparison": sample_comparison,
    "sample_counts": sample_counts,
    "fs_medians": fs_medians
}

# ─────────────────────────────────────────────
# 8) AR SUMMARY (for cross-ratio defaults)
# ─────────────────────────────────────────────
ar_summary_rows = read_csv("ar/ar_summary_by_ratio.csv")
ar_summary = []
for r in ar_summary_rows:
    ar_summary.append({
        "ratio": r["ratio"],
        "n": int(float(r.get("n","0"))),
        "phi1_median": float4(r.get("phi1_median","")),
        "sigma_median": float4(r.get("sigma_median","")),
        "signif_pct": float4(r.get("phi1_signif_pct",""))
    })

# ─────────────────────────────────────────────
# 9) SECTOR MEDIANS + GLOBAL MEDIANS + RANKS (for profile scatter)
# ─────────────────────────────────────────────
print("Computing sector medians, global medians and ranks...")

# Collect phi1/sigma per sector per ratio
from collections import defaultdict as dd2
sector_vals = dd2(lambda: dd2(lambda: {"phi1":[], "sigma":[]}))
global_vals = dd2(lambda: {"phi1":[], "sigma":[]})

for tk, c in companies.items():
    sector = c["sector"]
    for ratio in RATIOS:
        p = c["phi1"].get(ratio)
        s = c["sigma"].get(ratio)
        if p is not None and s is not None:
            sector_vals[sector][ratio]["phi1"].append(p)
            sector_vals[sector][ratio]["sigma"].append(s)
            global_vals[ratio]["phi1"].append(p)
            global_vals[ratio]["sigma"].append(s)

# Compute medians
sector_medians = {}
for sector, ratios in sector_vals.items():
    sector_medians[sector] = {}
    for ratio, vals in ratios.items():
        vals["phi1"].sort()
        vals["sigma"].sort()
        n = len(vals["phi1"])
        sector_medians[sector][ratio] = {
            "phi1": round(statistics.median(vals["phi1"]), 4),
            "sigma": round(statistics.median(vals["sigma"]), 4),
            "n": n
        }

global_medians = {}
for ratio, vals in global_vals.items():
    vals["phi1"].sort()
    vals["sigma"].sort()
    global_medians[ratio] = {
        "phi1": round(statistics.median(vals["phi1"]), 4),
        "sigma": round(statistics.median(vals["sigma"]), 4)
    }

# Compute ranks (lower phi1 = more corrective = rank 1, higher sigma = more volatile = rank 1)
ranks = {}  # {ratio: {ticker: {phi1_rank, sigma_rank, n}}}
for ratio in RATIOS:
    phi1_list = [(tk, c["phi1"].get(ratio)) for tk, c in companies.items() if c["phi1"].get(ratio) is not None]
    sigma_list = [(tk, c["sigma"].get(ratio)) for tk, c in companies.items() if c["sigma"].get(ratio) is not None]
    # Sort phi1 ascending (most negative first = rank 1)
    phi1_list.sort(key=lambda x: x[1])
    sigma_list.sort(key=lambda x: x[1], reverse=True)  # highest sigma = rank 1
    phi1_ranks = {tk: i+1 for i, (tk, _) in enumerate(phi1_list)}
    sigma_ranks = {tk: i+1 for i, (tk, _) in enumerate(sigma_list)}
    n = len(phi1_list)
    ranks[ratio] = {"phi1": phi1_ranks, "sigma": sigma_ranks, "n": n}

# Slim down ranks for JSON (only store per ticker)
ranks_json = {}
for ratio in RATIOS:
    ranks_json[ratio] = {"n": ranks[ratio]["n"]}
    for tk in companies:
        if tk not in ranks_json:
            pass  # will be accessed client-side from flat structure
    # Store as {ticker: [phi1_rank, sigma_rank]}
    ranks_json[ratio]["r"] = {tk: [ranks[ratio]["phi1"].get(tk), ranks[ratio]["sigma"].get(tk)]
                               for tk in companies if ranks[ratio]["phi1"].get(tk) is not None}

print(f"  {len(sector_medians)} sectors, {len(global_medians)} ratios with medians")

# ─────────────────────────────────────────────
# 10) MEDIAN COMPANIES (closest to global median per ratio)
# ─────────────────────────────────────────────
print("Finding median companies...")
median_companies = {}  # ratio -> ticker
for ratio in RATIOS:
    med_p = global_medians[ratio]["phi1"]
    med_s = global_medians[ratio]["sigma"]
    best_tk, best_dist = None, float('inf')
    for tk, c in companies.items():
        p = c["phi1"].get(ratio)
        s = c["sigma"].get(ratio)
        if p is None or s is None:
            continue
        dist = ((p - med_p)**2 + (s - med_s)**2)**0.5
        if dist < best_dist:
            best_tk, best_dist = tk, dist
    if best_tk:
        median_companies[ratio] = best_tk
        print(f"  {RATIO_LABELS[ratio]:15s}: {best_tk:8s} ({companies[best_tk].get('name', best_tk)})")

# ─────────────────────────────────────────────
# 11) GLOBAL AXIS RANGES (min/max across ALL companies for fixed-axis mode)
# ─────────────────────────────────────────────
all_phi1_vals = []
all_sigma_vals = []
for tk, c in companies.items():
    for ratio in RATIOS:
        p = c["phi1"].get(ratio)
        s = c["sigma"].get(ratio)
        if p is not None:
            all_phi1_vals.append(p)
        if s is not None:
            all_sigma_vals.append(s)

# Per-layer ranges for split view
layer_ranges = {}
LAYER_MAP = {
    "Profitabilität": ["ROA", "ROE", "EBIT_margin", "fcf_margin"],
    "Liquidität": ["current_ratio"],
    "Kapitalstruktur": ["debt_to_equity", "equity_ratio"]
}
for layer_name, layer_ratios in LAYER_MAP.items():
    lp, ls = [], []
    for tk, c in companies.items():
        for ratio in layer_ratios:
            p = c["phi1"].get(ratio)
            s = c["sigma"].get(ratio)
            if p is not None:
                lp.append(p)
            if s is not None:
                ls.append(s)
    if lp and ls:
        layer_ranges[layer_name] = {
            "phi1": [min(lp), max(lp)],
            "sigma": [min(ls), max(ls)]
        }

global_axis_ranges = {
    "all": {
        "phi1": [min(all_phi1_vals), max(all_phi1_vals)],
        "sigma": [min(all_sigma_vals), max(all_sigma_vals)]
    },
    "layers": layer_ranges
}
print(f"  Global axis ranges: phi1=[{global_axis_ranges['all']['phi1'][0]:.3f}, {global_axis_ranges['all']['phi1'][1]:.3f}], sigma=[{global_axis_ranges['all']['sigma'][0]:.3f}, {global_axis_ranges['all']['sigma'][1]:.3f}]")

print("All data loaded. Building HTML...")

# ─────────────────────────────────────────────
# BUILD HTML
# ─────────────────────────────────────────────

# Serialize data
data_json = json.dumps({
    "static": static,
    "levels": levels_dict,
    "raw_ts": raw_dict,
    "raw_labels": RAW_LABELS,
    "interdependence": interdependence,
    "validation": validation,
    "clustering": clustering,
    "robustness": robustness,
    "ar_summary": ar_summary,
    "thresholds": thresholds,
    "sector_medians": sector_medians,
    "global_medians": global_medians,
    "ranks": ranks_json,
    "median_companies": median_companies,
    "global_axis_ranges": global_axis_ranges
}, ensure_ascii=False, separators=(',',':'))

print(f"  JSON size: {len(data_json)/1024/1024:.1f} MB")

# ─────────────────────────────────────────────
# HTML TEMPLATE
# ─────────────────────────────────────────────
html_template = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Dynamik-Explorer v4 – Masterarbeit Tobias Mourier</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
:root {
  --bg: #f5f5f5; --bg2: #fff; --text: #333; --text2: #666; --text3: #888;
  --primary: #1a237e; --primary2: #283593; --accent: #ffab40;
  --border: #ddd; --border2: #eee; --hover: #e8eaf6;
  --ks: #1565c0; --kv: #e65100; --ps: #2e7d32; --pv: #c62828;
  --chart-bg: #fafafa;
}
[data-theme="dark"] {
  --bg: #121212; --bg2: #1e1e1e; --text: #e0e0e0; --text2: #aaa; --text3: #777;
  --primary: #7986cb; --primary2: #3949ab; --accent: #ffab40;
  --border: #333; --border2: #2a2a2a; --hover: #263238;
  --chart-bg: #1a1a1a;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',Arial,sans-serif; background:var(--bg); color:var(--text); overflow:hidden; height:100vh; }
.header { background:var(--primary2); color:white; padding:8px 20px; display:flex; justify-content:space-between; align-items:center; }
.header h1 { font-size:16px; } .header .sub { font-size:10px; opacity:.7; }
.header-right { display:flex; gap:8px; align-items:center; }
.hdr-btn { padding:4px 10px; border:1px solid rgba(255,255,255,.3); border-radius:4px; background:none; color:white; cursor:pointer; font-size:11px; }
.hdr-btn:hover { background:rgba(255,255,255,.15); }
.tab-bar { display:flex; background:var(--primary2); overflow-x:auto; }
.tab-btn { padding:6px 14px; color:rgba(255,255,255,.6); cursor:pointer; font-size:11px; border:none; background:none; border-bottom:2px solid transparent; white-space:nowrap; }
.tab-btn.active { color:white; border-bottom:2px solid var(--accent); }
.tab-btn:hover { color:white; background:rgba(255,255,255,.08); }
.controls { display:flex; gap:8px; padding:6px 14px; background:var(--bg2); border-bottom:1px solid var(--border); flex-wrap:wrap; align-items:flex-end; min-height:38px; }
.ctrl { display:flex; flex-direction:column; gap:2px; }
.ctrl label { font-size:9px; font-weight:600; text-transform:uppercase; color:var(--text3); }
.ctrl select,.ctrl input { padding:3px 6px; border:1px solid var(--border); border-radius:3px; font-size:11px; background:var(--bg2); color:var(--text); }
.ctrl select { min-width:120px; }
.toggle-btn { padding:3px 8px; border:1px solid var(--border); border-radius:3px; font-size:10px; cursor:pointer; background:var(--bg2); color:var(--text); }
.toggle-btn.active { background:var(--primary); color:white; border-color:var(--primary); }
.sector-bar { display:flex; gap:3px; padding:4px 14px; background:var(--bg2); border-bottom:1px solid var(--border2); flex-wrap:wrap; }
.s-btn { padding:2px 6px; border:1px solid var(--border); border-radius:10px; font-size:10px; cursor:pointer; background:var(--bg2); color:var(--text); }
.s-btn.active { background:var(--primary); color:white; border-color:var(--primary); }
.s-btn:hover { background:var(--hover); }
.main { display:flex; height:calc(100vh - 120px); }
.chart-area { flex:1; display:flex; flex-direction:column; min-width:0; }
.chart-container { flex:1; position:relative; }
.chart-container>div { width:100%; height:100%; }
.sidebar { width:280px; background:var(--bg2); border-left:1px solid var(--border); overflow-y:auto; padding:12px; flex-shrink:0; }
.sidebar h3 { font-size:12px; color:var(--primary); margin-bottom:5px; }
.search-wrap { position:relative; margin-bottom:8px; }
.search-wrap input { width:100%; padding:5px 8px; border:1px solid var(--border); border-radius:4px; font-size:11px; background:var(--bg2); color:var(--text); }
.search-results { position:absolute; top:100%; left:0; right:0; background:var(--bg2); border:1px solid var(--border); border-radius:0 0 4px 4px; max-height:200px; overflow-y:auto; z-index:100; display:none; }
.search-results.open { display:block; }
.sr-item { padding:4px 8px; cursor:pointer; font-size:10px; border-bottom:1px solid var(--border2); }
.sr-item:hover,.sr-item.sr-hl { background:var(--hover); }
.sr-item .sr-ticker { font-weight:700; }
.selected-companies { display:flex; flex-direction:column; gap:4px; margin-bottom:8px; }
.comp-card { display:flex; align-items:center; justify-content:space-between; padding:4px 7px; border-radius:4px; font-size:10px; cursor:pointer; }
.comp-card .ticker { font-weight:700; font-size:12px; } .comp-card .meta { color:var(--text2); font-size:9px; }
.comp-card .remove { cursor:pointer; color:#999; font-size:14px; } .comp-card .remove:hover { color:#f44336; }
.sector-group { margin:4px 0; border:1px solid var(--border2); border-radius:6px; overflow:hidden; }
.sector-group-header { display:flex; align-items:center; justify-content:space-between; padding:5px 8px; background:var(--bg); cursor:pointer; font-size:11px; font-weight:600; }
.sector-group-header:hover { background:var(--hover); }
.sector-group-body { max-height:200px; overflow-y:auto; }
.sector-group-body.collapsed { display:none; }
.ratio-checks { display:flex; gap:4px; flex-wrap:wrap; }
.ratio-checks label { font-size:9px; cursor:pointer; padding:2px 5px; border:1px solid var(--border); border-radius:3px; user-select:none; background:var(--bg2); color:var(--text); }
.ratio-checks label.active { background:var(--primary); color:white; border-color:var(--primary); }
.ratio-checks input { display:none; }
.profile-detail { font-size:10px; line-height:1.5; }
.profile-detail .big-ticker { font-size:18px; font-weight:700; color:var(--primary); }
.stat-row { display:flex; gap:4px; margin:4px 0; }
.stat-box { flex:1; background:var(--bg); border-radius:4px; padding:4px; text-align:center; }
.stat-box .v { font-size:13px; font-weight:700; color:var(--primary); } .stat-box .l { font-size:8px; color:var(--text3); text-transform:uppercase; }
.q-table { width:100%; border-collapse:collapse; margin-top:4px; }
.q-table td { padding:2px 4px; border-bottom:1px solid var(--border2); font-size:10px; }
.q-badge { display:inline-block; padding:1px 5px; border-radius:3px; color:white; font-size:9px; font-weight:600; }
.tab-panel { display:none; } .tab-panel.active { display:flex; flex-direction:column; height:100%; overflow-y:auto; }
/* Tour overlay */
.tour-overlay { position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,.5); z-index:1000; display:none; }
.tour-overlay.active { display:flex; align-items:center; justify-content:center; }
.tour-box { background:var(--bg2); border-radius:12px; padding:24px; max-width:500px; width:90%; box-shadow:0 8px 32px rgba(0,0,0,.3); }
.tour-box h3 { font-size:16px; color:var(--primary); margin-bottom:8px; }
.tour-box p { font-size:12px; line-height:1.6; margin-bottom:12px; color:var(--text); }
.tour-nav { display:flex; gap:8px; justify-content:flex-end; }
.tour-nav button { padding:6px 14px; border:none; border-radius:4px; cursor:pointer; font-size:11px; }
.tour-nav .next { background:var(--primary); color:white; } .tour-nav .skip { background:var(--border); color:var(--text); }
.tour-progress { font-size:10px; color:var(--text3); margin-bottom:8px; }
/* Compare mode */
.compare-container { display:flex; gap:8px; height:100%; }
.compare-container > div { flex:1; }
</style>
</head>
<body>
<!-- HEADER -->
<div class="header">
  <div>
    <h1>Dynamik-Explorer v4</h1>
    <div class="sub">Masterarbeit Tobias Mourier – TH Wildau · 932 Unternehmen × 7 Kennzahlen</div>
  </div>
  <div class="header-right">
    <button class="hdr-btn" id="tourBtn" title="Guided Tour">▶ Tour</button>
    <button class="hdr-btn" id="compareBtn" title="Vergleichsmodus">⇔ Vergleich</button>
    <button class="hdr-btn" id="exportBtn" title="Chart als PNG">📷 Export</button>
    <button class="hdr-btn" id="csvExportBtn" title="Daten als CSV">📊 CSV</button>
    <button class="hdr-btn" id="darkBtn" title="Dark Mode">🌙</button>
  </div>
</div>

<!-- TAB BAR -->
<div class="tab-bar">
  <button class="tab-btn active" data-tab="scatter">📊 Scatter</button>
  <button class="tab-btn" data-tab="crossratio">📈 Cross-Ratio</button>
  <button class="tab-btn" data-tab="timeline">⏳ Zeitverlauf AR</button>
  <button class="tab-btn" data-tab="levels">📉 Levels</button>
  <button class="tab-btn" data-tab="rawdata">📋 Rohdaten</button>
  <button class="tab-btn" data-tab="interdependence">🔗 Interdependenz</button>
  <button class="tab-btn" data-tab="validation">✅ Validierung</button>
  <button class="tab-btn" data-tab="robustness">🔒 Robustheit</button>
</div>

<!-- MAIN CONTENT -->
<div class="main">
<div class="chart-area">

<!-- TAB 1: SCATTER -->
<div class="tab-panel active" id="panel-scatter">
  <div class="controls" id="ctrl-scatter">
    <div class="ctrl"><label>Kennzahl</label><select id="ratioSel"></select></div>
    <div class="ctrl"><label>X-Achse</label><select id="xSel"><option value="phi1">φ₁</option><option value="sigma">σ(ΔY)</option></select></div>
    <div class="ctrl"><label>Y-Achse</label><select id="ySel"><option value="sigma">σ(ΔY)</option><option value="phi1">φ₁</option></select></div>
    <div class="ctrl"><label>Farbe</label><select id="colorSel"><option value="quadrant">Quadrant</option><option value="sector">Sektor</option><option value="kmeans">K-Means</option></select></div>
    <div class="ctrl"><label>Cluster</label><button class="toggle-btn" id="clusterOverlay">K-Means</button></div>
  </div>
  <div class="sector-bar" id="sectorBar"></div>
  <div class="chart-container"><div id="scatterChart"></div></div>
</div>

<!-- TAB 2: CROSS-RATIO -->
<div class="tab-panel" id="panel-crossratio">
  <div class="controls" id="ctrl-crossratio">
    <div class="ctrl"><label>Ansicht</label>
      <select id="crView"><option value="bar">Balken</option><option value="radar">Radar</option><option value="profil">Profil-Scatter</option></select>
    </div>
    <div class="ctrl" id="crMetricCtrl"><label>Metrik</label>
      <select id="crMetric"><option value="phi1">φ₁</option><option value="sigma">σ(ΔY)</option><option value="both">Beide</option></select>
    </div>
    <div class="ctrl" id="crLayerCtrl" style="display:none"><label>Schichten</label>
      <div style="display:flex;gap:4px;">
        <button class="toggle-btn active" id="crLayerAll">Alle</button>
        <button class="toggle-btn" id="crLayerSplit">Nach Schicht</button>
      </div>
    </div>
    <div class="ctrl" id="crBenchCtrl" style="display:none"><label>Referenz</label>
      <select id="crBenchSelect" multiple size="3" style="min-width:160px;font-size:11px;">
        <option value="global" selected>Gesamt-Median (932)</option>
      </select>
      <div style="font-size:8px;color:var(--text3);margin-top:2px">Strg+Klick für Mehrfachauswahl</div>
    </div>
    <div class="ctrl" id="crAxisCtrl" style="display:none"><label>Achsen</label>
      <div style="display:flex;gap:4px;">
        <button class="toggle-btn active" id="crAxisDynamic">Dynamisch</button>
        <button class="toggle-btn" id="crAxisFixed">Fest (Global)</button>
      </div>
    </div>
  </div>
  <div class="sector-bar" id="crSectorBar" style="display:none"></div>
  <div id="crossMainWrap" style="flex:1;min-height:0;overflow:hidden;position:relative">
    <div id="crossChartWrap" style="width:100%;height:100%;overflow:hidden"><div id="crossChart" style="width:100%;height:100%"></div></div>
  </div>
  <div id="crossBoxWrap" style="display:none;height:250px;flex-shrink:0;border-top:1px solid var(--border2);padding-top:4px"><div id="crossBoxChart" style="height:100%;width:100%"></div></div>
</div>

<!-- TAB 3: ZEITVERLAUF AR -->
<div class="tab-panel" id="panel-timeline">
  <div class="controls" id="ctrl-timeline">
    <div class="ctrl"><label>AR-Ordnung</label>
      <div style="display:flex;align-items:center;gap:4px;">
        <button class="toggle-btn" id="arDown">−</button>
        <span id="arVal" style="font-weight:700;font-size:14px;min-width:16px;text-align:center;">1</span>
        <button class="toggle-btn" id="arUp">+</button>
      </div>
    </div>
    <div class="ctrl"><label>Metrik</label><select id="tlMetric"><option value="phi">φ₁</option><option value="sigma">σ(ΔY)</option></select></div>
    <div class="ctrl"><label>Kennzahlen</label><div class="ratio-checks" id="tlRatioChecks"></div></div>
    <div class="ctrl"><label>Optionen</label>
      <div style="display:flex;gap:4px;">
        <button class="toggle-btn" id="tlConfBand">±σ Band</button>
        <button class="toggle-btn" id="tlMedian">Median</button>
        <button class="toggle-btn" id="tlAllPhi">Alle φ</button>
      </div>
    </div>
  </div>
  <div class="chart-container"><div id="timelineChart"></div></div>
</div>

<!-- TAB 4: LEVELS -->
<div class="tab-panel" id="panel-levels">
  <div class="controls" id="ctrl-levels">
    <div class="ctrl"><label>Kennzahlen</label><div class="ratio-checks" id="lvRatioChecks"></div></div>
    <div class="ctrl"><label>Modus</label>
      <div style="display:flex;gap:4px;">
        <button class="toggle-btn active" id="lvLevels">Levels</button>
        <button class="toggle-btn" id="lvDelta">Δ</button>
        <button class="toggle-btn" id="lvNorm">z-Norm</button>
      </div>
    </div>
  </div>
  <div class="chart-container"><div id="levelsChart"></div></div>
</div>

<!-- TAB 5: ROHDATEN -->
<div class="tab-panel" id="panel-rawdata">
  <div class="controls" id="ctrl-rawdata">
    <div class="ctrl"><label>Datenreihen</label><div class="ratio-checks" id="rawChecks"></div></div>
    <div class="ctrl"><label>Modus</label>
      <div style="display:flex;gap:4px;">
        <button class="toggle-btn active" id="rawAbs">Absolut</button>
        <button class="toggle-btn" id="rawGrowth">Q/Q %</button>
        <button class="toggle-btn" id="rawIndex">Index=100</button>
      </div>
    </div>
  </div>
  <div class="chart-container"><div id="rawChart"></div></div>
</div>

<!-- TAB 6: INTERDEPENDENZ -->
<div class="tab-panel" id="panel-interdependence">
  <div class="controls" id="ctrl-interdependence">
    <div class="ctrl"><label>Ansicht</label>
      <select id="idView">
        <option value="heatmap_phi1">Heatmap φ₁-Korr.</option>
        <option value="heatmap_sigma">Heatmap σ-Korr.</option>
        <option value="cramers">Cramér's V</option>
      </select>
    </div>
  </div>
  <div class="chart-container"><div id="interdepChart"></div></div>
</div>

<!-- TAB 7: VALIDIERUNG -->
<div class="tab-panel" id="panel-validation">
  <div class="controls" id="ctrl-validation">
    <div class="ctrl"><label>Ansicht</label>
      <select id="valView">
        <option value="chi2">χ² Sektor-Assoziation</option>
        <option value="size">Größeneffekte</option>
        <option value="consistency">Konsistenz</option>
        <option value="kmeans">K-Means</option>
      </select>
    </div>
    <div class="ctrl" id="valRatioCtrl"><label>Kennzahl</label><select id="valRatio"></select></div>
    <div class="ctrl" id="valSizeCtrl" style="display:none"><label>Größe</label>
      <select id="valSizeVar"><option value="market_cap">Marktkapitalisierung</option><option value="employees">Mitarbeiter</option></select>
    </div>
    <div class="ctrl" id="valTargetCtrl" style="display:none"><label>Ziel</label>
      <select id="valTarget"><option value="phi1">φ₁</option><option value="sigma_diff">σ(ΔY)</option></select>
    </div>
  </div>
  <div class="chart-container"><div id="validationChart"></div></div>
</div>

<!-- TAB 8: ROBUSTHEIT -->
<div class="tab-panel" id="panel-robustness">
  <div class="controls" id="ctrl-robustness">
    <div class="ctrl"><label>Ansicht</label>
      <select id="robView">
        <option value="sample">Sample-Sensitivität</option>
        <option value="finserv">Financial Services</option>
        <option value="funnel">Stichproben-Trichter</option>
      </select>
    </div>
  </div>
  <div class="chart-container"><div id="robustnessChart"></div></div>
</div>

</div><!-- /chart-area -->

<!-- SIDEBAR (global) -->
<div class="sidebar">
  <div class="search-wrap">
    <input type="text" id="searchInput" placeholder="Name, Ticker oder Branche suchen..." autocomplete="off">
    <div class="search-results" id="searchResults"></div>
  </div>
  <h3>Ausgewählt <span id="selCount">(0)</span></h3>
  <div class="selected-companies" id="selectedList"></div>
  <div id="profileDetail" class="profile-detail"></div>
</div>
</div><!-- /main -->

<!-- TOUR OVERLAY -->
<div class="tour-overlay" id="tourOverlay">
  <div class="tour-box">
    <div class="tour-progress" id="tourProgress"></div>
    <h3 id="tourTitle"></h3>
    <p id="tourText"></p>
    <div class="tour-nav">
      <button class="skip" id="tourSkip">Beenden</button>
      <button class="skip" id="tourPrev">← Zurück</button>
      <button class="next" id="tourNext">Weiter →</button>
    </div>
  </div>
</div>

<script>
// ═══════════════════════════════════════════
// DATA
// ═══════════════════════════════════════════
const D=__DATA_JSON__;

const S=D.static, COMP=S.companies, RATIOS=S.ratios, RL=S.ratio_labels;
const LEVELS=D.levels, RAW=D.raw_ts, RAW_LABELS=D.raw_labels;
const INTER=D.interdependence, VAL=D.validation, CLUST=D.clustering, ROB=D.robustness;
const THRESH=D.thresholds;

// ═══════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════
const QC={"KORREKTIV-STABIL":"var(--ks)","KORREKTIV-VOLATIL":"var(--kv)","PERSISTENT-STABIL":"var(--ps)","PERSISTENT-VOLATIL":"var(--pv)"};
const QCH={"KORREKTIV-STABIL":"#1565c0","KORREKTIV-VOLATIL":"#e65100","PERSISTENT-STABIL":"#2e7d32","PERSISTENT-VOLATIL":"#c62828"};
const QL={"KORREKTIV-STABIL":"Korr.-Stabil","KORREKTIV-VOLATIL":"Korr.-Volatil","PERSISTENT-STABIL":"Pers.-Stabil","PERSISTENT-VOLATIL":"Pers.-Volatil"};
const DASHES=["solid","dash","dot","dashdot","longdash"];
const PALETTE=["#e6194b","#3cb44b","#4363d8","#f58231","#911eb4","#42d4f4","#f032e6","#bfef45","#fabed4","#469990","#dcbeff","#9A6324","#800000","#aaffc3","#808000","#000075"];
const SECTOR_COLORS={};
const EVENTS=[{q:"2001Q4",l:"Dot-Com"},{q:"2009Q2",l:"GFC"},{q:"2020Q3",l:"COVID"}];

// ═══════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════
let selectedCompanies=[]; // [{ticker, color, visible}]
let arOrder=1;
let activeTab="scatter";
let renderedTabs=new Set();
let darkMode=false;
let lvMode="levels"; // "levels"|"delta"|"norm"
let rawMode="abs"; // "abs"|"growth"|"index"

// Gather sectors
const allSectors=new Set();
Object.values(COMP).forEach(c=>{if(c.sector)allSectors.add(c.sector);});
const sectorList=[...allSectors].sort();
let activeSectors=new Set(sectorList);
sectorList.forEach((s,i)=>{SECTOR_COLORS[s]=PALETTE[i%PALETTE.length];});
const tickers=Object.keys(COMP).sort();
let loadedSectorGroups=new Set(); // sectors loaded as a group on cross-ratio tab
let collapsedGroups=new Set(); // collapsed sector groups in sidebar

// ═══════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════
function visCo(){return selectedCompanies.filter(c=>c.visible);}
function qBadge(q){const c=QCH[q]||"#999";const l=QL[q]||q;return `<span class="q-badge" style="background:${c}">${l}</span>`;}
function fmt(v,d=4){if(v==null)return"–";return Number(v).toFixed(d);}
function fmtPct(v){if(v==null)return"–";return (v*100).toFixed(1)+"%";}
function fmtBig(v){if(v==null)return"–";if(Math.abs(v)>=1e9)return (v/1e9).toFixed(1)+"B";if(Math.abs(v)>=1e6)return (v/1e6).toFixed(1)+"M";if(Math.abs(v)>=1e3)return (v/1e3).toFixed(0)+"K";return v.toFixed(0);}
function getPlotlyTheme(){
  const d=darkMode;
  return {paper_bgcolor:d?"#1e1e1e":"#fff",plot_bgcolor:d?"#1a1a1a":"#fafafa",
    font:{color:d?"#e0e0e0":"#333"},
    xaxis:{gridcolor:d?"#333":"#eee",zerolinecolor:d?"#444":"#ccc"},
    yaxis:{gridcolor:d?"#333":"#eee",zerolinecolor:d?"#444":"#ccc"}
  };
}
function eventShapes(){
  return EVENTS.map(e=>({type:"line",x0:e.q,x1:e.q,y0:0,y1:1,yref:"paper",line:{color:"#ef5350",dash:"dot",width:1}}));
}
function eventAnnotations(){
  return EVENTS.map(e=>({x:e.q,y:1,yref:"paper",text:e.l,showarrow:false,font:{size:9,color:"#ef5350"},yanchor:"bottom"}));
}

// ═══════════════════════════════════════════
// TAB SWITCHING
// ═══════════════════════════════════════════
document.querySelectorAll(".tab-btn").forEach(btn=>{
  btn.addEventListener("click",()=>{
    document.querySelectorAll(".tab-btn").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    const tab=btn.dataset.tab;
    document.querySelectorAll(".tab-panel").forEach(p=>p.classList.remove("active"));
    document.getElementById("panel-"+tab).classList.add("active");
    activeTab=tab;
    updateCurrentTab();
    updateHash();
  });
});

function updateCurrentTab(){
  if(activeTab==="scatter")updateScatter();
  else if(activeTab==="crossratio")updateCrossRatio();
  else if(activeTab==="timeline")updateTimeline();
  else if(activeTab==="levels")updateLevels();
  else if(activeTab==="rawdata")updateRawData();
  else if(activeTab==="interdependence")updateInterdependence();
  else if(activeTab==="validation")updateValidation();
  else if(activeTab==="robustness")updateRobustness();
}

// ═══════════════════════════════════════════
// SIDEBAR: Search & Selection (GLOBAL)
// ═══════════════════════════════════════════
const searchInput=document.getElementById("searchInput");
const searchResults=document.getElementById("searchResults");
let srIdx=-1;

searchInput.addEventListener("input",()=>{
  const q=searchInput.value.trim().toUpperCase();
  searchResults.innerHTML="";srIdx=-1;
  if(q.length<1){searchResults.classList.remove("open");return;}
  const matches=tickers.filter(t=>t.startsWith(q)||COMP[t].name.toUpperCase().includes(q)||COMP[t].sector.toUpperCase().includes(q)||COMP[t].industry.toUpperCase().includes(q)).slice(0,20);
  if(!matches.length){searchResults.classList.remove("open");return;}
  matches.forEach(t=>{
    const d=document.createElement("div");d.className="sr-item";
    d.innerHTML=`<span class="sr-ticker">${t}</span> <span style="color:var(--text2);font-size:9px">${COMP[t].name}</span><br><span style="color:var(--text3);font-size:8px">${COMP[t].sector} · ${COMP[t].industry}</span>`;
    d.addEventListener("click",()=>{addCompany(t);searchInput.value="";searchResults.classList.remove("open");});
    searchResults.appendChild(d);
  });
  searchResults.classList.add("open");
});

searchInput.addEventListener("keydown",e=>{
  const items=searchResults.querySelectorAll(".sr-item");
  if(e.key==="ArrowDown"){e.preventDefault();srIdx=Math.min(srIdx+1,items.length-1);items.forEach((it,i)=>it.classList.toggle("sr-hl",i===srIdx));}
  else if(e.key==="ArrowUp"){e.preventDefault();srIdx=Math.max(srIdx-1,0);items.forEach((it,i)=>it.classList.toggle("sr-hl",i===srIdx));}
  else if(e.key==="Enter"&&srIdx>=0){items[srIdx].click();}
  else if(e.key==="Escape"){searchResults.classList.remove("open");}
});

document.addEventListener("click",e=>{if(!e.target.closest(".search-wrap"))searchResults.classList.remove("open");});

function addCompany(ticker){
  if(selectedCompanies.find(c=>c.ticker===ticker))return;
  const color=PALETTE[selectedCompanies.length%PALETTE.length];
  selectedCompanies.push({ticker,color,visible:true});
  renderSidebar();updateCurrentTab();updateHash();updateBenchSelect();
}

function removeCompany(ticker){
  const removed=selectedCompanies.find(c=>c.ticker===ticker);
  selectedCompanies=selectedCompanies.filter(c=>c.ticker!==ticker);
  // Clean up sector group if last member removed
  if(removed?.sectorGroup){
    const remaining=selectedCompanies.filter(c=>c.sectorGroup===removed.sectorGroup);
    if(!remaining.length)loadedSectorGroups.delete(removed.sectorGroup);
  }
  renderSidebar();renderCrSectorBar();updateCurrentTab();updateHash();updateBenchSelect();
}
function toggleCompanyVisibility(ticker){
  const c=selectedCompanies.find(c=>c.ticker===ticker);
  if(c)c.visible=!c.visible;
  renderSidebar();updateCurrentTab();
}
function toggleSectorGroup(sector){
  if(loadedSectorGroups.has(sector)){
    // Remove all companies from this sector group
    selectedCompanies=selectedCompanies.filter(c=>c.sectorGroup!==sector);
    loadedSectorGroups.delete(sector);
  } else {
    // Add all companies in this sector
    const existing=new Set(selectedCompanies.map(c=>c.ticker));
    const sectorTickers=tickers.filter(t=>COMP[t].sector===sector&&!existing.has(t));
    const baseIdx=selectedCompanies.length;
    sectorTickers.forEach((t,i)=>{
      selectedCompanies.push({ticker:t,color:SECTOR_COLORS[sector]||PALETTE[(baseIdx+i)%PALETTE.length],visible:true,sectorGroup:sector});
    });
    loadedSectorGroups.add(sector);
  }
  renderSidebar();renderCrSectorBar();updateCurrentTab();updateBenchSelect();
}
function toggleSectorGroupVisibility(sector){
  const members=selectedCompanies.filter(c=>c.sectorGroup===sector);
  const allVisible=members.every(c=>c.visible);
  members.forEach(c=>{c.visible=!allVisible;});
  renderSidebar();updateCurrentTab();
}
function renderCrSectorBar(){
  const bar=document.getElementById("crSectorBar");
  const view=document.getElementById("crView").value;
  bar.style.display=view==="profil"?"":"none";
  if(view!=="profil")return;
  bar.innerHTML="";
  sectorList.forEach(s=>{
    const cnt=tickers.filter(t=>COMP[t].sector===s).length;
    const b=document.createElement("button");b.className="s-btn"+(loadedSectorGroups.has(s)?" active":"");
    b.textContent=s+" ("+cnt+")";b.style.borderColor=SECTOR_COLORS[s];
    if(loadedSectorGroups.has(s))b.style.background=SECTOR_COLORS[s]+"33";
    b.addEventListener("click",()=>toggleSectorGroup(s));
    bar.appendChild(b);
  });
}

function makeCompCard(c){
  const d=document.createElement("div");d.className="comp-card";
  d.style.background=c.visible?c.color+"22":"transparent";
  d.style.borderLeft="3px solid "+(c.visible?c.color:"#999");
  d.style.opacity=c.visible?"1":".45";
  const co=COMP[c.ticker];
  d.innerHTML=`<div style="flex:1;min-width:0"><span class="ticker" style="color:${c.visible?c.color:'#999'}">${co.name||c.ticker}</span><div class="meta">${c.ticker}${c.sectorGroup?'':' · '+co.sector}</div></div><span class="eye-btn" title="${c.visible?'Ausblenden':'Einblenden'}" style="cursor:pointer;padding:2px 5px;font-size:13px;opacity:.6">${c.visible?'👁':'👁‍🗨'}</span><span class="remove" style="cursor:pointer;padding:2px 4px;color:#999">✕</span>`;
  d.querySelector(".remove").addEventListener("click",e=>{e.stopPropagation();removeCompany(c.ticker);});
  d.querySelector(".eye-btn").addEventListener("click",e=>{e.stopPropagation();toggleCompanyVisibility(c.ticker);});
  d.addEventListener("click",()=>showProfile(c.ticker));
  return d;
}
function renderSidebar(){
  document.getElementById("selCount").textContent="("+selectedCompanies.length+")";
  const list=document.getElementById("selectedList");
  list.innerHTML="";

  // Separate: individual companies vs sector-group companies
  const individuals=selectedCompanies.filter(c=>!c.sectorGroup);
  const groupedSectors=[...loadedSectorGroups].sort();

  // Render individual companies first
  individuals.forEach(c=>{
    list.appendChild(makeCompCard(c));
  });

  // Render sector groups
  groupedSectors.forEach(sector=>{
    const members=selectedCompanies.filter(c=>c.sectorGroup===sector);
    if(!members.length)return;
    const visCount=members.filter(c=>c.visible).length;
    const isCollapsed=collapsedGroups.has(sector);
    const allVis=visCount===members.length;

    const grp=document.createElement("div");grp.className="sector-group";
    const hdr=document.createElement("div");hdr.className="sector-group-header";
    hdr.style.borderLeft="3px solid "+(SECTOR_COLORS[sector]||"#999");
    hdr.innerHTML=`<span style="flex:1">${isCollapsed?'▶':'▼'} ${sector} <span style="color:var(--text3);font-weight:400">(${visCount}/${members.length} sichtbar)</span></span><span class="sg-eye" style="cursor:pointer;padding:2px 5px;font-size:13px;opacity:.6" title="Alle ein-/ausblenden">${allVis?'👁':'👁‍🗨'}</span><span class="sg-remove" style="cursor:pointer;padding:2px 4px;color:#999;font-size:14px" title="Gruppe entfernen">✕</span>`;
    hdr.querySelector(".sg-eye").addEventListener("click",e=>{e.stopPropagation();toggleSectorGroupVisibility(sector);});
    hdr.querySelector(".sg-remove").addEventListener("click",e=>{e.stopPropagation();toggleSectorGroup(sector);});
    hdr.addEventListener("click",()=>{
      if(collapsedGroups.has(sector))collapsedGroups.delete(sector);else collapsedGroups.add(sector);
      renderSidebar();
    });
    grp.appendChild(hdr);

    if(!isCollapsed){
      const body=document.createElement("div");body.className="sector-group-body";
      members.forEach(c=>body.appendChild(makeCompCard(c)));
      grp.appendChild(body);
    }
    list.appendChild(grp);
  });

  if(selectedCompanies.length===1)showProfile(selectedCompanies[0].ticker);
  else if(selectedCompanies.length===0)document.getElementById("profileDetail").innerHTML="";
}

function showProfile(ticker){
  const c=COMP[ticker];if(!c)return;
  const pd=document.getElementById("profileDetail");
  let h=`<div class="big-ticker">${c.name||ticker}</div><div style="color:var(--text2)">${ticker} · ${c.industry} · ${c.sector}</div>`;
  h+=`<div class="stat-row"><div class="stat-box"><div class="v">${fmtBig(c.market_cap)}</div><div class="l">MarketCap</div></div>`;
  h+=`<div class="stat-box"><div class="v">${c.employees?fmtBig(c.employees):"–"}</div><div class="l">Mitarbeiter</div></div>`;
  h+=`<div class="stat-box"><div class="v">${(c.consistency*100).toFixed(0)}%</div><div class="l">Konsistenz</div></div></div>`;
  h+=`<table class="q-table"><tr><td><b>Ratio</b></td><td><b>Quadrant</b></td><td><b>φ₁</b></td><td><b>σ</b></td></tr>`;
  RATIOS.forEach(r=>{
    h+=`<tr><td>${RL[r]}</td><td>${qBadge(c.quadrants[r])}</td><td>${fmt(c.phi1[r])}</td><td>${fmt(c.sigma[r])}</td></tr>`;
  });
  h+=`</table>`;
  if(c.kmeans!=null)h+=`<div style="margin-top:6px">K-Means Cluster: <b>${c.kmeans}</b></div>`;
  pd.innerHTML=h;
}

// ═══════════════════════════════════════════
// SECTOR BAR (for scatter)
// ═══════════════════════════════════════════
function renderSectorBar(){
  const bar=document.getElementById("sectorBar");bar.innerHTML="";
  // Count companies per sector for current ratio
  const ratio=document.getElementById("ratioSel").value||RATIOS[0];
  const counts={};sectorList.forEach(s=>{counts[s]=0;});
  tickers.forEach(t=>{const c=COMP[t];if(c.phi1[ratio]!=null)counts[c.sector]=(counts[c.sector]||0)+1;});
  // All button
  const allBtn=document.createElement("button");allBtn.className="s-btn"+(activeSectors.size===sectorList.length?" active":"");
  allBtn.textContent="Alle";allBtn.addEventListener("click",()=>{
    if(activeSectors.size===sectorList.length)activeSectors.clear();else sectorList.forEach(s=>activeSectors.add(s));
    renderSectorBar();updateScatter();
  });bar.appendChild(allBtn);
  sectorList.forEach(s=>{
    const b=document.createElement("button");b.className="s-btn"+(activeSectors.has(s)?" active":"");
    b.textContent=s+" ("+counts[s]+")";b.style.borderColor=SECTOR_COLORS[s];
    if(activeSectors.has(s))b.style.background=SECTOR_COLORS[s]+"33";
    b.addEventListener("click",()=>{
      if(activeSectors.has(s))activeSectors.delete(s);else activeSectors.add(s);
      renderSectorBar();updateScatter();
    });
    // Hover: highlight sector points in red on the scatter
    b.addEventListener("mouseenter",()=>{highlightSector(s);});
    b.addEventListener("mouseleave",()=>{clearSectorHighlight();});
    bar.appendChild(b);
  });
}

let _sectorHighlightTrace=null;
function highlightSector(sector){
  if(activeTab!=="scatter")return;
  const ratio=document.getElementById("ratioSel").value||RATIOS[0];
  const xKey=document.getElementById("xSel").value;
  const yKey=document.getElementById("ySel").value;
  const pts=tickers.filter(t=>COMP[t].sector===sector).map(t=>{
    const c=COMP[t];
    const xv=xKey==="phi1"?c.phi1[ratio]:c.sigma[ratio];
    const yv=yKey==="phi1"?c.phi1[ratio]:c.sigma[ratio];
    return (xv!=null&&yv!=null)?{x:xv,y:yv,t:t,n:c.name||t}:null;
  }).filter(Boolean);
  if(!pts.length)return;
  const el=document.getElementById("scatterChart");
  const nTraces=el.data?el.data.length:0;
  // Add highlight trace
  Plotly.addTraces("scatterChart",{
    x:pts.map(p=>p.x),y:pts.map(p=>p.y),text:pts.map(p=>p.n),customdata:pts.map(p=>[p.t]),
    name:"⬤ "+sector,type:"scatter",mode:"markers",
    marker:{color:"#ff1744",size:8,line:{color:"white",width:1.5},opacity:.9},
    hovertemplate:"<b>%{text}</b> (%{customdata[0]})<br>"+sector+"<extra></extra>",
    showlegend:false
  });
  _sectorHighlightTrace=nTraces;// index of the added trace
}
function clearSectorHighlight(){
  if(_sectorHighlightTrace!=null){
    try{Plotly.deleteTraces("scatterChart",_sectorHighlightTrace);}catch(e){}
    _sectorHighlightTrace=null;
  }
}

// ═══════════════════════════════════════════
// TAB 1: SCATTER
// ═══════════════════════════════════════════
function updateScatter(){
  const ratio=document.getElementById("ratioSel").value||RATIOS[0];
  const xKey=document.getElementById("xSel").value;
  const yKey=document.getElementById("ySel").value;
  const colorBy=document.getElementById("colorSel").value;
  const showCluster=document.getElementById("clusterOverlay").classList.contains("active");
  const th=THRESH[ratio]||{};
  const theme=getPlotlyTheme();

  // Group by color
  const groups={};
  tickers.forEach(t=>{
    const c=COMP[t];
    if(!activeSectors.has(c.sector))return;
    const xv=xKey==="phi1"?c.phi1[ratio]:c.sigma[ratio];
    const yv=yKey==="phi1"?c.phi1[ratio]:c.sigma[ratio];
    if(xv==null||yv==null)return;
    let grp;
    if(colorBy==="quadrant")grp=c.quadrants[ratio]||"?";
    else if(colorBy==="sector")grp=c.sector;
    else grp="Cluster "+(c.kmeans!=null?c.kmeans:"?");
    if(!groups[grp])groups[grp]=[];
    groups[grp].push({x:xv,y:yv,t:t,sector:c.sector,industry:c.industry});
  });

  const traces=[];
  Object.keys(groups).sort().forEach(grp=>{
    const pts=groups[grp];
    let color;
    if(colorBy==="quadrant")color=QCH[grp]||"#999";
    else if(colorBy==="sector")color=SECTOR_COLORS[grp]||"#999";
    else color=grp.includes("0")?"#1565c0":"#c62828";
    traces.push({
      x:pts.map(p=>p.x),y:pts.map(p=>p.y),
      text:pts.map(p=>COMP[p.t]?.name||p.t),customdata:pts.map(p=>[p.sector,p.industry,p.t]),
      name:colorBy==="quadrant"?(QL[grp]||grp):grp,
      type:"scatter",mode:"markers",
      marker:{color:color,size:5,opacity:.7},
      hovertemplate:"<b>%{text}</b> (%{customdata[2]})<br>%{customdata[0]} · %{customdata[1]}<br>"+(xKey==="phi1"?"φ₁":"σ")+": %{x:.4f}<br>"+(yKey==="phi1"?"φ₁":"σ")+": %{y:.4f}<extra>%{fullData.name}</extra>"
    });
  });

  // Highlight selected
  visCo().forEach(sc=>{
    const c=COMP[sc.ticker];if(!c)return;
    const xv=xKey==="phi1"?c.phi1[ratio]:c.sigma[ratio];
    const yv=yKey==="phi1"?c.phi1[ratio]:c.sigma[ratio];
    if(xv==null||yv==null)return;
    const cName=c.name||sc.ticker;
    traces.push({x:[xv],y:[yv],text:[cName],name:cName,type:"scatter",mode:"markers+text",
      marker:{color:sc.color,size:12,line:{color:"white",width:2}},
      textposition:"top center",textfont:{size:10,color:sc.color,weight:"bold"},showlegend:false});
  });

  const shapes=[];
  // Quadrant lines
  if(th.phi1_med!=null&&xKey==="phi1")shapes.push({type:"line",x0:th.phi1_med,x1:th.phi1_med,y0:0,y1:1,yref:"paper",line:{color:"#999",dash:"dash",width:1}});
  if(th.sigma_med!=null&&yKey==="sigma")shapes.push({type:"line",x0:0,x1:1,xref:"paper",y0:th.sigma_med,y1:th.sigma_med,line:{color:"#999",dash:"dash",width:1}});
  if(th.phi1_med!=null&&yKey==="phi1")shapes.push({type:"line",x0:0,x1:1,xref:"paper",y0:th.phi1_med,y1:th.phi1_med,line:{color:"#999",dash:"dash",width:1}});
  if(th.sigma_med!=null&&xKey==="sigma")shapes.push({type:"line",x0:th.sigma_med,x1:th.sigma_med,y0:0,y1:1,yref:"paper",line:{color:"#999",dash:"dash",width:1}});

  // Fixed axis ranges across all ratios for comparability
  const axisRange={
    phi1:[-1.05, 0.55],
    sigma:[-0.05, 1.5]
  };
  const layout={
    ...theme,
    title:{text:(RL[ratio]||ratio)+" – "+(xKey==="phi1"?"φ₁":"σ(ΔY)")+" vs "+(yKey==="phi1"?"φ₁":"σ(ΔY)"),font:{size:13}},
    xaxis:{...theme.xaxis,title:xKey==="phi1"?"φ₁ (AR-Koeffizient)":"σ(ΔY) (Volatilität)",range:axisRange[xKey]},
    yaxis:{...theme.yaxis,title:yKey==="phi1"?"φ₁ (AR-Koeffizient)":"σ(ΔY) (Volatilität)",range:axisRange[yKey]},
    shapes:shapes,
    legend:{orientation:"h",y:-.12,x:.5,xanchor:"center",font:{size:9}},
    margin:{t:40,r:10,b:60,l:55},
    hovermode:"closest",
    transition:{duration:400}
  };
  Plotly.react("scatterChart",traces,layout,{responsive:true});

  // Click to add company
  const el=document.getElementById("scatterChart");
  el.removeAllListeners&&el.removeAllListeners("plotly_click");
  el.on("plotly_click",data=>{
    if(data.points&&data.points[0]){const pt=data.points[0];const tk=pt.customdata?.[2]||pt.text;addCompany(tk);}
  });
}

// ═══════════════════════════════════════════
// TAB 2: CROSS-RATIO
// ═══════════════════════════════════════════
// Layer definitions
const LAYERS={
  "Profitabilität":["ROA","ROE","EBIT_margin","fcf_margin"],
  "Liquidität":["current_ratio"],
  "Kapitalstruktur":["debt_to_equity","equity_ratio"]
};
const LAYER_ORDER=["Profitabilität","Liquidität","Kapitalstruktur"];
const SYMBOLS=["circle","diamond","square","triangle-up","star","hexagon","cross"];
const COMP_SYMBOLS=["circle","diamond","square","triangle-up","star","hexagon"];

function updateCrossRatio(){
  const view=document.getElementById("crView").value;
  const metric=document.getElementById("crMetric").value;
  const theme=getPlotlyTheme();

  // Show/hide controls depending on view
  document.getElementById("crMetricCtrl").style.display=view==="profil"?"none":"";
  document.getElementById("crLayerCtrl").style.display=view==="profil"?"":"none";
  document.getElementById("crBenchCtrl").style.display=view==="profil"?"":"none";
  document.getElementById("crAxisCtrl").style.display=view==="profil"?"":"none";
  const showBox=view==="profil"&&visCo().length>0;
  document.getElementById("crossBoxWrap").style.display=showBox?"block":"none";
  renderCrSectorBar();

  if(!visCo().length){
    // Show aggregate medians
    const summaryData=D.ar_summary;
    const traces=[];
    document.getElementById("crossBoxWrap").style.display="none";
    if(view==="profil"){
      Plotly.react("crossChart",[],{...theme,title:{text:"Wähle mindestens ein Unternehmen für den Profil-Scatter.",font:{size:13}},
        xaxis:{visible:false},yaxis:{visible:false},margin:{t:50}},{responsive:true});
      return;
    }
    if(metric==="phi1"||metric==="both"){
      traces.push({
        x:summaryData.map(r=>RL[r.ratio]||r.ratio),y:summaryData.map(r=>r.phi1_median),
        name:"φ₁ Median",type:"bar",marker:{color:"#1565c0"}
      });
    }
    if(metric==="sigma"||metric==="both"){
      traces.push({
        x:summaryData.map(r=>RL[r.ratio]||r.ratio),y:summaryData.map(r=>r.sigma_median),
        name:"σ Median",type:"bar",marker:{color:"#e65100"}
      });
    }
    Plotly.react("crossChart",traces,{...theme,title:{text:"Mediane über alle Unternehmen",font:{size:13}},barmode:"group",
      xaxis:{...theme.xaxis},yaxis:{...theme.yaxis,title:metric==="sigma"?"σ(ΔY)":"φ₁"},
      margin:{t:40,r:10,b:40,l:50},legend:{orientation:"h",y:-.1,x:.5,xanchor:"center"}},{responsive:true});
    return;
  }

  if(view==="profil"){
    renderProfileScatter(theme);
    renderProfileBoxplot(theme);
    setTimeout(()=>{Plotly.Plots.resize("crossChart");Plotly.Plots.resize("crossBoxChart");},50);
  } else if(view==="radar"){
    const traces=[];
    visCo().forEach(sc=>{
      const c=COMP[sc.ticker];if(!c)return;
      const cats=RATIOS.map(r=>RL[r]||r);
      const cN=c.name||sc.ticker;
      if(metric==="phi1"||metric==="both"){
        traces.push({type:"scatterpolar",r:RATIOS.map(r=>c.phi1[r]),theta:cats,fill:"toself",
          name:cN+" φ₁",line:{color:sc.color},opacity:.6});
      }
      if(metric==="sigma"||metric==="both"){
        traces.push({type:"scatterpolar",r:RATIOS.map(r=>c.sigma[r]),theta:cats,fill:"toself",
          name:cN+" σ",line:{color:sc.color,dash:"dash"},opacity:.6});
      }
    });
    Plotly.react("crossChart",traces,{...theme,polar:{radialaxis:{visible:true},bgcolor:theme.plot_bgcolor},
      title:{text:"Radar – "+visCo().map(c=>(COMP[c.ticker]?.name||c.ticker)).join(", "),font:{size:13}},
      margin:{t:50,r:40,b:40,l:40},legend:{font:{size:9}}},{responsive:true});
  } else {
    // Bar chart per selected company
    const traces=[];
    visCo().forEach(sc=>{
      const c=COMP[sc.ticker];if(!c)return;
      const cN=c.name||sc.ticker;
      if(metric==="phi1"||metric==="both"){
        traces.push({x:RATIOS.map(r=>RL[r]),y:RATIOS.map(r=>c.phi1[r]),name:cN+" φ₁",type:"bar",
          marker:{color:sc.color,opacity:metric==="both"?1:.8}});
      }
      if(metric==="sigma"||metric==="both"){
        traces.push({x:RATIOS.map(r=>RL[r]),y:RATIOS.map(r=>c.sigma[r]),name:cN+" σ",type:"bar",
          marker:{color:sc.color,opacity:.5,pattern:{shape:"/"}}});
      }
    });
    Plotly.react("crossChart",traces,{...theme,barmode:"group",
      title:{text:"Cross-Ratio – "+visCo().map(c=>(COMP[c.ticker]?.name||c.ticker)).join(", "),font:{size:13}},
      xaxis:{...theme.xaxis},yaxis:{...theme.yaxis,title:metric==="sigma"?"σ(ΔY)":"φ₁"},
      margin:{t:40,r:10,b:40,l:50},legend:{orientation:"h",y:-.1,x:.5,xanchor:"center",font:{size:9}}},{responsive:true});
  }
}

// ═══════════════════════════════════════════
// PROFILE SCATTER (Company × all 7 Ratios in φ₁ vs σ space)
// ═══════════════════════════════════════════
let crLayerMode="all"; // "all" or "split"
let crFixedAxes=false; // false=dynamic, true=fixed global ranges

function renderProfileScatter(theme){
  const benchSel=document.getElementById("crBenchSelect");
  const benchVals=new Set([...benchSel.selectedOptions].map(o=>o.value));
  const showGlobalMed=benchVals.has("global");
  const benchSectors=[...benchVals].filter(v=>v.startsWith("sector:")).map(v=>v.slice(7));
  const SM=D.sector_medians;
  const GM=D.global_medians;
  const RK=D.ranks;

  if(crLayerMode==="split"){
    renderProfileSplit(theme,benchSectors,showGlobalMed,SM,GM,RK);
    return;
  }

  // Single chart: all 7 ratios
  const traces=[];

  // Ratio number mapping for median markers
  const RATIO_NUM={};RATIOS.forEach((r,i)=>{RATIO_NUM[r]=String(i+1);});

  // Company traces – fill=company color, border=quadrant color
  visCo().forEach((sc,ci)=>{
    const c=COMP[sc.ticker];if(!c)return;
    const sym=COMP_SYMBOLS[ci%COMP_SYMBOLS.length];
    const cName=c.name||sc.ticker;
    const xs=[],ys=[],texts=[],borderColors=[],customdata=[];
    RATIOS.forEach((r,ri)=>{
      const p=c.phi1[r], s=c.sigma[r];
      if(p==null||s==null)return;
      xs.push(p);ys.push(s);
      const q=c.quadrants[r]||"?";
      borderColors.push(QCH[q]||"#999");
      const rank=RK[r]?.r?.[sc.ticker];
      const pctPhi1=rank?Math.round((1-rank[0]/RK[r].n)*100):null;
      const pctSigma=rank?Math.round((1-rank[1]/RK[r].n)*100):null;
      const rTxt=rank?'Rang φ₁: '+rank[0]+'/'+RK[r].n+' ('+pctPhi1+'%)'+'  |  Rang σ: '+rank[1]+'/'+RK[r].n+' ('+pctSigma+'%)':'';
      const qLabel=QL[q]||q;
      texts.push(RL[r]||r);
      customdata.push([qLabel,rTxt,cName,RL[r]||r,sc.ticker]);
    });
    // Points: fill = company, thick border = quadrant
    traces.push({
      x:xs,y:ys,text:texts,customdata:customdata,
      name:cName+' ('+sc.ticker+')',type:"scatter",mode:"markers+text",
      marker:{color:sc.color,size:14,symbol:sym,line:{color:borderColors,width:3}},
      textposition:"top center",textfont:{size:9,color:sc.color},
      hovertemplate:'<b>%{customdata[2]}</b> (%{customdata[4]})<br>%{customdata[3]}<br>φ₁: %{x:.4f} · σ: %{y:.4f}<br>Quadrant: %{customdata[0]}<br>%{customdata[1]}<extra></extra>'
    });
    // Connecting line (profile polygon)
    traces.push({
      x:xs,y:ys,type:"scatter",mode:"lines",
      line:{color:sc.color,width:1.5,dash:"dot"},opacity:.35,showlegend:false,hoverinfo:"skip"
    });
  });

  // Sector median reference (numbered markers, teal color)
  if(benchSectors.length){
    benchSectors.forEach(sector=>{
      const sm=SM[sector];if(!sm)return;
      RATIOS.forEach((r,ri)=>{
        if(!sm[r])return;
        traces.push({
          x:[sm[r].phi1],y:[sm[r].sigma],text:[RATIO_NUM[r]],
          name:ri===0?'Ø '+sector+' (n='+(sm[r]?.n||'?')+')':undefined,showlegend:ri===0,legendgroup:'sm_'+sector,
          type:"scatter",mode:"markers+text",
          marker:{color:"#00897b",size:20,symbol:"square",opacity:.55,line:{color:"#00695c",width:1.5}},
          textfont:{size:11,color:"#fff",family:"Arial Black"},textposition:"middle center",
          hovertemplate:'<b>Sektor-Median '+sector+'</b><br>'+RATIO_NUM[r]+' = '+(RL[r]||r)+'<br>φ₁: %{x:.4f} · σ: %{y:.4f}<br>n='+sm[r].n+'<extra></extra>'
        });
      });
    });
  }

  // Global median reference (numbered markers, purple color)
  if(showGlobalMed){
    RATIOS.forEach((r,ri)=>{
      if(!GM[r])return;
      traces.push({
        x:[GM[r].phi1],y:[GM[r].sigma],text:[RATIO_NUM[r]],
        name:ri===0?'Ø Gesamt (932)':undefined,showlegend:ri===0,legendgroup:'gm',
        type:"scatter",mode:"markers+text",
        marker:{color:"#7b1fa2",size:16,symbol:"diamond",opacity:.45,line:{color:"#4a148c",width:1.5}},
        textfont:{size:9,color:"#fff",family:"Arial Black"},textposition:"middle center",
        hovertemplate:'<b>Gesamt-Median</b><br>'+RATIO_NUM[r]+' = '+(RL[r]||r)+'<br>φ₁: %{x:.4f} · σ: %{y:.4f}<extra></extra>'
      });
    });
  }

  // Quadrant background colors – four colored zones
  const shapes=[];
  const TH=D.thresholds;
  const allPhi1Med=RATIOS.map(r=>TH[r]?.phi1_med).filter(v=>v!=null);
  const allSigMed=RATIOS.map(r=>TH[r]?.sigma_med).filter(v=>v!=null);
  const phi1Avg=allPhi1Med.reduce((a,b)=>a+b,0)/allPhi1Med.length;
  const sigAvg=allSigMed.reduce((a,b)=>a+b,0)/allSigMed.length;
  const xL=-1.05,xR=0.55,yB=-0.05,yT=1.5;
  const qAlpha=darkMode?'0.08':'0.05';
  // KV: left-top (korrektiv + volatil)
  shapes.push({type:"rect",x0:xL,x1:phi1Avg,y0:sigAvg,y1:yT,fillcolor:'rgba(230,81,0,'+qAlpha+')',line:{width:0},layer:"below"});
  // KS: left-bottom (korrektiv + stabil)
  shapes.push({type:"rect",x0:xL,x1:phi1Avg,y0:yB,y1:sigAvg,fillcolor:'rgba(21,101,192,'+qAlpha+')',line:{width:0},layer:"below"});
  // PV: right-top (persistent + volatil)
  shapes.push({type:"rect",x0:phi1Avg,x1:xR,y0:sigAvg,y1:yT,fillcolor:'rgba(198,40,40,'+qAlpha+')',line:{width:0},layer:"below"});
  // PS: right-bottom (persistent + stabil)
  shapes.push({type:"rect",x0:phi1Avg,x1:xR,y0:yB,y1:sigAvg,fillcolor:'rgba(46,125,50,'+qAlpha+')',line:{width:0},layer:"below"});
  // Divider lines
  shapes.push({type:"line",x0:phi1Avg,x1:phi1Avg,y0:yB,y1:yT,line:{color:darkMode?"#555":"#bbb",dash:"dash",width:1}});
  shapes.push({type:"line",x0:xL,x1:xR,y0:sigAvg,y1:sigAvg,line:{color:darkMode?"#555":"#bbb",dash:"dash",width:1}});

  const titleParts=visCo().map(sc=>{const n=COMP[sc.ticker]?.name;return n?n+' ('+sc.ticker+')':sc.ticker;}).join(" vs ");
  // Ratio number legend annotation
  const ratioLegendText=RATIOS.map((r,i)=>(i+1)+'='+RL[r]).join('  ');

  // Axis ranges: fixed (global) or dynamic
  const GAR=D.global_axis_ranges;
  let xaxCfg,yaxCfg;
  if(crFixedAxes){
    const pad=0.05;
    const xr=[GAR.all.phi1[0]-pad, GAR.all.phi1[1]+pad];
    const yr=[GAR.all.sigma[0]-(GAR.all.sigma[1]*0.05), GAR.all.sigma[1]*1.05];
    xaxCfg={...theme.xaxis,title:"φ₁ (AR-Koeffizient)",range:xr};
    yaxCfg={...theme.yaxis,title:"σ(ΔY) (Volatilität)",range:yr};
    // Adjust quadrant backgrounds to cover full fixed range
    shapes.length=0;
    shapes.push({type:"rect",x0:xr[0],x1:phi1Avg,y0:sigAvg,y1:yr[1],fillcolor:'rgba(230,81,0,'+qAlpha+')',line:{width:0},layer:"below"});
    shapes.push({type:"rect",x0:xr[0],x1:phi1Avg,y0:yr[0],y1:sigAvg,fillcolor:'rgba(21,101,192,'+qAlpha+')',line:{width:0},layer:"below"});
    shapes.push({type:"rect",x0:phi1Avg,x1:xr[1],y0:sigAvg,y1:yr[1],fillcolor:'rgba(198,40,40,'+qAlpha+')',line:{width:0},layer:"below"});
    shapes.push({type:"rect",x0:phi1Avg,x1:xr[1],y0:yr[0],y1:sigAvg,fillcolor:'rgba(46,125,50,'+qAlpha+')',line:{width:0},layer:"below"});
    shapes.push({type:"line",x0:phi1Avg,x1:phi1Avg,y0:yr[0],y1:yr[1],line:{color:darkMode?"#555":"#bbb",dash:"dash",width:1}});
    shapes.push({type:"line",x0:xr[0],x1:xr[1],y0:sigAvg,y1:sigAvg,line:{color:darkMode?"#555":"#bbb",dash:"dash",width:1}});
  } else {
    xaxCfg={...theme.xaxis,title:"φ₁ (AR-Koeffizient)",autorange:true};
    yaxCfg={...theme.yaxis,title:"σ(ΔY) (Volatilität)",autorange:true};
  }

  Plotly.react("crossChart",traces,{...theme,
    title:{text:"Profil-Scatter: "+titleParts,font:{size:12}},
    xaxis:xaxCfg,
    yaxis:yaxCfg,
    shapes:shapes,
    legend:{font:{size:9},x:1.02,y:1,xanchor:"left"},
    margin:{t:40,r:150,b:70,l:55},
    hovermode:"closest",
    annotations:[
      {x:0.15,y:0.98,text:"← KORREKTIV",showarrow:false,font:{size:9,color:QCH["KORREKTIV-VOLATIL"]},opacity:.6,xref:"paper",yref:"paper"},
      {x:0.85,y:0.98,text:"PERSISTENT →",showarrow:false,font:{size:9,color:QCH["PERSISTENT-VOLATIL"]},opacity:.6,xref:"paper",yref:"paper"},
      {x:0.01,y:0.75,text:"VOLATIL ↑",showarrow:false,font:{size:8,color:"#aaa"},textangle:-90,xref:"paper",yref:"paper"},
      {x:0.01,y:0.25,text:"↓ STABIL",showarrow:false,font:{size:8,color:"#aaa"},textangle:-90,xref:"paper",yref:"paper"},
      {x:0.5,y:-0.08,text:ratioLegendText,showarrow:false,font:{size:8,color:darkMode?"#888":"#999"},xref:"paper",yref:"paper"}
    ]
  },{responsive:true});
}

function renderProfileSplit(theme,benchSectors,showGlobalMed,SM,GM,RK){
  // Three subplots side by side (using Plotly subplots)
  const traces=[];
  const annotations=[];

  LAYER_ORDER.forEach((layer,li)=>{
    const layerRatios=LAYERS[layer];
    const xaxis=li===0?"x":"x"+(li+1);
    const yaxis=li===0?"y":"y"+(li+1);

    // Company points
    const RATIO_NUM_S={};RATIOS.forEach((r,i)=>{RATIO_NUM_S[r]=String(i+1);});
    visCo().forEach((sc,ci)=>{
      const c=COMP[sc.ticker];if(!c)return;
      const sym=COMP_SYMBOLS[ci%COMP_SYMBOLS.length];
      const cName=c.name||sc.ticker;
      const xs=[],ys=[],texts=[],borderColors=[],cd=[];
      layerRatios.forEach(r=>{
        const p=c.phi1[r],s=c.sigma[r];
        if(p==null||s==null)return;
        xs.push(p);ys.push(s);texts.push(RL[r]||r);
        const q=c.quadrants[r]||"?";
        borderColors.push(QCH[q]||"#999");
        const rank=RK[r]?.r?.[sc.ticker];
        const pctP=rank?Math.round((1-rank[0]/RK[r].n)*100):null;
        const pctS=rank?Math.round((1-rank[1]/RK[r].n)*100):null;
        cd.push([QL[q]||q,rank?'φ₁: '+rank[0]+'/'+RK[r].n+' ('+pctP+'%) | σ: '+rank[1]+'/'+RK[r].n+' ('+pctS+'%)':'?',cName,RL[r]||r,sc.ticker]);
      });
      traces.push({
        x:xs,y:ys,text:texts,customdata:cd,
        name:li===0?cName+' ('+sc.ticker+')':undefined,showlegend:li===0,
        type:"scatter",mode:"markers+text",xaxis:xaxis,yaxis:yaxis,
        marker:{color:sc.color,size:14,symbol:sym,line:{color:borderColors,width:3}},
        textposition:"top center",textfont:{size:9,color:sc.color},
        hovertemplate:'<b>%{customdata[2]}</b> (%{customdata[4]})<br>%{customdata[3]}<br>φ₁: %{x:.4f} · σ: %{y:.4f}<br>Quadrant: %{customdata[0]}<br>%{customdata[1]}<extra></extra>'
      });
      // Connecting line
      if(xs.length>1){
        traces.push({x:xs,y:ys,type:"scatter",mode:"lines",xaxis:xaxis,yaxis:yaxis,
          line:{color:sc.color,width:1,dash:"dot"},opacity:.3,showlegend:false,hoverinfo:"skip"});
      }
    });

    // Sector medians (numbered, teal)
    if(benchSectors.length){
      benchSectors.forEach(sector=>{
        const sm=SM[sector];if(!sm)return;
        layerRatios.forEach((r,ri)=>{
          if(!sm[r])return;
          traces.push({x:[sm[r].phi1],y:[sm[r].sigma],text:[RATIO_NUM_S[r]],
            name:(li===0&&ri===0)?'Ø '+sector:undefined,showlegend:(li===0&&ri===0),legendgroup:'sm_'+sector,
            type:"scatter",mode:"markers+text",xaxis:xaxis,yaxis:yaxis,
            marker:{color:"#00897b",size:18,symbol:"square",opacity:.55,line:{color:"#00695c",width:1.5}},
            textfont:{size:10,color:"#fff",family:"Arial Black"},textposition:"middle center",
            hovertemplate:'Sektor '+sector+'<br>'+RATIO_NUM_S[r]+'='+(RL[r]||r)+': φ₁=%{x:.4f}, σ=%{y:.4f}<extra></extra>'});
        });
      });
    }
    // Global medians (numbered, purple)
    if(showGlobalMed){
      layerRatios.forEach((r,ri)=>{
        if(!GM[r])return;
        traces.push({x:[GM[r].phi1],y:[GM[r].sigma],text:[RATIO_NUM_S[r]],
          name:(li===0&&ri===0)?'Ø Gesamt':undefined,showlegend:(li===0&&ri===0),legendgroup:'gm',
          type:"scatter",mode:"markers+text",xaxis:xaxis,yaxis:yaxis,
          marker:{color:"#7b1fa2",size:14,symbol:"diamond",opacity:.45,line:{color:"#4a148c",width:1.5}},
          textfont:{size:9,color:"#fff",family:"Arial Black"},textposition:"middle center",
          hovertemplate:'Gesamt<br>'+RATIO_NUM_S[r]+'='+(RL[r]||r)+': φ₁=%{x:.4f}, σ=%{y:.4f}<extra></extra>'});
      });
    }

    // Layer title annotation
    annotations.push({text:'<b>'+layer+'</b>',x:0.5,y:1.08,xref:xaxis.replace("x","x")+" domain",yref:yaxis.replace("y","y")+" domain",
      showarrow:false,font:{size:11,color:theme.font?.color||"#333"}});
  });

  // Quadrant background colors for each subplot
  const shapes=[];
  const TH=D.thresholds;
  const allPhi1Med=RATIOS.map(r=>TH[r]?.phi1_med).filter(v=>v!=null);
  const allSigMed=RATIOS.map(r=>TH[r]?.sigma_med).filter(v=>v!=null);
  const phi1Avg=allPhi1Med.reduce((a,b)=>a+b,0)/allPhi1Med.length;
  const sigAvg=allSigMed.reduce((a,b)=>a+b,0)/allSigMed.length;
  const qAlpha=darkMode?'0.08':'0.05';

  const GAR=D.global_axis_ranges;
  const layerNames=["Profitabilität","Liquidität","Kapitalstruktur"];

  [0,1,2].forEach(li=>{
    const xref=li===0?"x":"x"+(li+1);
    const yref=li===0?"y":"y"+(li+1);
    let xL,xR,yB,yT;
    if(crFixedAxes){
      const lr=GAR.layers[layerNames[li]]||GAR.all;
      const padX=0.05, padY=(lr.sigma[1]-lr.sigma[0])*0.05||0.05;
      xL=lr.phi1[0]-padX; xR=lr.phi1[1]+padX;
      yB=lr.sigma[0]-padY; yT=lr.sigma[1]+padY;
    } else {
      xL=-1.05;xR=0.55;yB=-0.05;yT=1.5;
    }
    // KV: left-top
    shapes.push({type:"rect",x0:xL,x1:phi1Avg,y0:sigAvg,y1:yT,xref:xref,yref:yref,fillcolor:'rgba(230,81,0,'+qAlpha+')',line:{width:0},layer:"below"});
    // KS: left-bottom
    shapes.push({type:"rect",x0:xL,x1:phi1Avg,y0:yB,y1:sigAvg,xref:xref,yref:yref,fillcolor:'rgba(21,101,192,'+qAlpha+')',line:{width:0},layer:"below"});
    // PV: right-top
    shapes.push({type:"rect",x0:phi1Avg,x1:xR,y0:sigAvg,y1:yT,xref:xref,yref:yref,fillcolor:'rgba(198,40,40,'+qAlpha+')',line:{width:0},layer:"below"});
    // PS: right-bottom
    shapes.push({type:"rect",x0:phi1Avg,x1:xR,y0:yB,y1:sigAvg,xref:xref,yref:yref,fillcolor:'rgba(46,125,50,'+qAlpha+')',line:{width:0},layer:"below"});
    // Divider lines
    shapes.push({type:"line",x0:phi1Avg,x1:phi1Avg,y0:yB,y1:yT,xref:xref,yref:yref,line:{color:darkMode?"#555":"#bbb",dash:"dash",width:1}});
    shapes.push({type:"line",x0:xL,x1:xR,y0:sigAvg,y1:sigAvg,xref:xref,yref:yref,line:{color:darkMode?"#555":"#bbb",dash:"dash",width:1}});
  });

  // Axis configs per subplot
  function splitAxisCfg(li){
    if(crFixedAxes){
      const lr=GAR.layers[layerNames[li]]||GAR.all;
      const padX=0.05, padY=(lr.sigma[1]-lr.sigma[0])*0.05||0.05;
      return {
        xax:{...theme.xaxis,title:"φ₁",range:[lr.phi1[0]-padX,lr.phi1[1]+padX]},
        yax:{...theme.yaxis,title:"σ(ΔY)",range:[lr.sigma[0]-padY,lr.sigma[1]+padY]}
      };
    }
    return {
      xax:{...theme.xaxis,title:"φ₁",autorange:true},
      yax:{...theme.yaxis,title:"σ(ΔY)",autorange:true}
    };
  }
  const a0=splitAxisCfg(0),a1=splitAxisCfg(1),a2=splitAxisCfg(2);

  const layout={...theme,
    title:{text:"Profil-Scatter nach Schicht: "+visCo().map(sc=>{const n=COMP[sc.ticker]?.name;return n?n:sc.ticker;}).join(" vs "),font:{size:12}},
    grid:{rows:1,columns:3,pattern:"independent",xgap:.08},
    xaxis:a0.xax, yaxis:a0.yax,
    xaxis2:a1.xax, yaxis2:a1.yax,
    xaxis3:a2.xax, yaxis3:a2.yax,
    shapes:shapes,
    legend:{font:{size:9},x:1.02,y:1,xanchor:"left"},
    margin:{t:55,r:150,b:55,l:55},
    hovermode:"closest",
    annotations:annotations
  };
  Plotly.react("crossChart",traces,layout,{responsive:true});
}

// ═══════════════════════════════════════════
// PROFILE BOXPLOT (distribution of visible companies per ratio)
// ═══════════════════════════════════════════
function renderProfileBoxplot(theme){
  const vc=visCo();
  if(!vc.length){Plotly.react("crossBoxChart",[],{},{ responsive:true});return;}
  const traces=[];
  // Collect phi1 and sigma per ratio for visible companies
  RATIOS.forEach((r,ri)=>{
    const phi1Vals=[],sigmaVals=[],names=[];
    vc.forEach(sc=>{
      const c=COMP[sc.ticker];if(!c)return;
      const p=c.phi1[r],s=c.sigma[r];
      if(p!=null)phi1Vals.push(p);
      if(s!=null)sigmaVals.push(s);
    });
    const label=RL[r]||r;
    // phi1 boxes
    if(vc.length>=4){
      traces.push({y:phi1Vals,type:"box",name:label,
        marker:{color:"#1565c0"},boxpoints:"all",jitter:.3,pointpos:-1.5,
        line:{width:1},fillcolor:"rgba(21,101,192,0.15)",
        xaxis:"x",yaxis:"y",legendgroup:"phi1",showlegend:ri===0,
        hovertemplate:'φ₁ '+label+': %{y:.4f}<extra></extra>'});
    } else {
      // Strip plot for few companies
      traces.push({y:phi1Vals,x:phi1Vals.map(()=>label),type:"scatter",mode:"markers",
        name:ri===0?"φ₁":undefined,showlegend:ri===0,legendgroup:"phi1",
        marker:{color:"#1565c0",size:8},xaxis:"x",yaxis:"y",
        hovertemplate:'φ₁ '+label+': %{y:.4f}<extra></extra>'});
    }
    // sigma boxes
    if(vc.length>=4){
      traces.push({y:sigmaVals,type:"box",name:label,
        marker:{color:"#e65100"},boxpoints:"all",jitter:.3,pointpos:-1.5,
        line:{width:1},fillcolor:"rgba(230,81,0,0.15)",
        xaxis:"x2",yaxis:"y2",legendgroup:"sigma",showlegend:ri===0,
        hovertemplate:'σ '+label+': %{y:.4f}<extra></extra>'});
    } else {
      traces.push({y:sigmaVals,x:sigmaVals.map(()=>label),type:"scatter",mode:"markers",
        name:ri===0?"σ":undefined,showlegend:ri===0,legendgroup:"sigma",
        marker:{color:"#e65100",size:8},xaxis:"x2",yaxis:"y2",
        hovertemplate:'σ '+label+': %{y:.4f}<extra></extra>'});
    }
  });
  const nLabel=vc.length===1?vc[0].ticker:vc.length+' Unternehmen';
  Plotly.react("crossBoxChart",traces,{...theme,
    title:{text:'Verteilung φ₁ und σ über '+nLabel,font:{size:11}},
    grid:{rows:1,columns:2,pattern:"independent",xgap:.1},
    xaxis:{...theme.xaxis,title:""},yaxis:{...theme.yaxis,title:"φ₁",zeroline:true},
    xaxis2:{...theme.xaxis,title:""},yaxis2:{...theme.yaxis,title:"σ(ΔY)",zeroline:true},
    legend:{orientation:"h",y:-.15,x:.5,xanchor:"center",font:{size:9}},
    margin:{t:30,r:20,b:50,l:50},
    annotations:[
      {text:"<b>φ₁ (Persistenz)</b>",x:0.22,y:1.05,xref:"paper",yref:"paper",showarrow:false,font:{size:10,color:theme.font?.color||"#333"}},
      {text:"<b>σ (Volatilität)</b>",x:0.78,y:1.05,xref:"paper",yref:"paper",showarrow:false,font:{size:10,color:theme.font?.color||"#333"}}
    ]
  },{responsive:true});
}

// ═══════════════════════════════════════════
// TAB 3: ZEITVERLAUF AR (Rolling)
// ═══════════════════════════════════════════
function computeRollingAR(values,p,win=20){
  // Returns {phi:[phi1,...], sigma:[], quarters:[]} for rolling AR(p) on first-differenced data
  const n=values.length;
  if(n<win+p+1)return null;
  // First differences
  const diffs=[];
  for(let i=1;i<n;i++){if(values[i]!=null&&values[i-1]!=null)diffs.push(values[i]-values[i-1]);else diffs.push(null);}
  const results={quarters:[],phi1:[],sigma:[],phi_all:[]};
  for(let end=win+p;end<=diffs.length;end++){
    const slice=diffs.slice(end-win,end);
    if(slice.some(v=>v==null))continue;
    // OLS: Y_t = c + phi1*Y_t-1 + ... + phip*Y_t-p
    const Y=[];const X=[];
    for(let t=p;t<slice.length;t++){
      Y.push(slice[t]);
      const row=[1];
      for(let lag=1;lag<=p;lag++)row.push(slice[t-lag]);
      X.push(row);
    }
    if(Y.length<p+2)continue;
    // Solve via normal equations (X'X)^-1 X'Y
    const k=p+1;
    const XtX=Array.from({length:k},()=>new Float64Array(k));
    const XtY=new Float64Array(k);
    for(let i=0;i<Y.length;i++){
      for(let a=0;a<k;a++){
        XtY[a]+=X[i][a]*Y[i];
        for(let b=0;b<k;b++)XtX[a][b]+=X[i][a]*X[i][b];
      }
    }
    // Gauss elimination
    const aug=XtX.map((row,i)=>[...row,XtY[i]]);
    for(let col=0;col<k;col++){
      let maxR=col;for(let r=col+1;r<k;r++)if(Math.abs(aug[r][col])>Math.abs(aug[maxR][col]))maxR=r;
      [aug[col],aug[maxR]]=[aug[maxR],aug[col]];
      if(Math.abs(aug[col][col])<1e-12)continue;
      for(let r=0;r<k;r++){
        if(r===col)continue;
        const f=aug[r][col]/aug[col][col];
        for(let c=col;c<=k;c++)aug[r][c]-=f*aug[col][c];
      }
    }
    const beta=aug.map((row,i)=>row[k]/row[i]);
    // Residuals
    let sse=0;
    for(let i=0;i<Y.length;i++){
      let pred=0;for(let j=0;j<k;j++)pred+=beta[j]*X[i][j];
      sse+=(Y[i]-pred)**2;
    }
    const sigma=Math.sqrt(sse/Math.max(1,Y.length-k));
    results.quarters.push(end);// index into original
    results.phi1.push(beta[1]);
    results.sigma.push(sigma);
    results.phi_all.push(beta.slice(1));// all phi coefficients
  }
  return results;
}

function updateTimeline(){
  const ratios=[...tlActiveRatios];
  const p=arOrder;
  const metric=document.getElementById("tlMetric").value;
  const showConf=document.getElementById("tlConfBand").classList.contains("active");
  const showMedian=document.getElementById("tlMedian").classList.contains("active");
  const showAllPhi=document.getElementById("tlAllPhi").classList.contains("active");
  const theme=getPlotlyTheme();

  if(!visCo().length||!ratios.length){
    Plotly.react("timelineChart",[],{...theme,title:{text:"Wähle Unternehmen und Kennzahlen.",font:{size:13}},
      xaxis:{visible:false},yaxis:{visible:false},margin:{t:50}},{responsive:true});return;
  }

  const traces=[];
  const allMedianData={};// ratio -> {quarters:[], values:[]}

  visCo().forEach((sc,ci)=>{
    ratios.forEach((ratio,ri)=>{
      const lv=LEVELS[sc.ticker]?.[ratio];
      if(!lv||!lv.values.length)return;
      const ar=computeRollingAR(lv.values,p);
      if(!ar||!ar.quarters.length)return;
      const quarters=ar.quarters.map(i=>lv.quarters[i]);
      const vals=metric==="phi"?ar.phi1:ar.sigma;
      const dash=DASHES[ri%DASHES.length];
      const cNm=COMP[sc.ticker]?.name||sc.ticker;
      traces.push({x:quarters,y:vals,name:cNm+" · "+(RL[ratio]||ratio),type:"scatter",mode:"lines",
        line:{color:sc.color,width:2,dash:dash},
        hovertemplate:"<b>"+cNm+"</b> "+(RL[ratio]||ratio)+"<br>%{x}: %{y:.4f}<extra></extra>"});

      // Confidence band
      if(showConf&&metric==="phi"){
        const upper=ar.phi1.map((v,i)=>v+ar.sigma[i]);
        const lower=ar.phi1.map((v,i)=>v-ar.sigma[i]);
        traces.push({x:quarters.concat([...quarters].reverse()),y:upper.concat([...lower].reverse()),
          fill:"toself",fillcolor:sc.color+"15",line:{color:"transparent"},showlegend:false,hoverinfo:"skip",type:"scatter"});
      }

      // All phi coefficients
      if(showAllPhi&&p>1&&metric==="phi"){
        for(let pi=1;pi<p;pi++){
          const phiVals=ar.phi_all.map(a=>a[pi]);
          traces.push({x:quarters,y:phiVals,name:cNm+" φ"+(pi+1)+" "+(RL[ratio]||ratio),type:"scatter",mode:"lines",
            line:{color:sc.color,width:1,dash:"dot"},opacity:.5,showlegend:true});
        }
      }

      // Collect for median
      if(showMedian){
        if(!allMedianData[ratio])allMedianData[ratio]=[];
        allMedianData[ratio].push({quarters:quarters,values:vals});
      }
    });
  });

  // Median lines (across all tickers, not just selected - would need precomputation)
  // For now, compute median over all tickers for first selected ratio
  if(showMedian&&ratios.length>0){
    ratios.forEach(ratio=>{
      // Quick median: compute AR for a sample of tickers
      const allVals={};
      const sampleTickers=tickers.slice(0,100);// limit for performance
      sampleTickers.forEach(t=>{
        const lv=LEVELS[t]?.[ratio];
        if(!lv)return;
        const ar=computeRollingAR(lv.values,p);
        if(!ar)return;
        ar.quarters.forEach((qi,i)=>{
          const q=lv.quarters[qi];
          if(!allVals[q])allVals[q]=[];
          allVals[q].push(metric==="phi"?ar.phi1[i]:ar.sigma[i]);
        });
      });
      const qs=Object.keys(allVals).sort();
      const medians=qs.map(q=>{
        const v=allVals[q].sort((a,b)=>a-b);
        return v[Math.floor(v.length/2)];
      });
      traces.push({x:qs,y:medians,name:"Median "+(RL[ratio]||ratio),type:"scatter",mode:"lines",
        line:{color:"#999",width:2,dash:"longdash"},opacity:.6});
    });
  }

  const tl=ratios.map(r=>RL[r]||r).join(", ");
  Plotly.react("timelineChart",traces,{...theme,
    title:{text:tl+" – AR("+p+") "+(metric==="phi"?"φ₁":"σ(ΔY)")+" Rolling 20Q",font:{size:13}},
    xaxis:{...theme.xaxis,title:"Quartal",tickangle:-45},
    yaxis:{...theme.yaxis,title:metric==="phi"?"φ₁":"σ(ΔY)"},
    shapes:eventShapes(),annotations:eventAnnotations(),
    legend:{orientation:"h",y:-.18,x:.5,xanchor:"center",font:{size:9}},
    margin:{t:40,r:10,b:70,l:50},hovermode:"x unified"
  },{responsive:true});
}

// ═══════════════════════════════════════════
// TAB 4: LEVELS
// ═══════════════════════════════════════════
function updateLevels(){
  const ratios=[...lvActiveRatios];
  const theme=getPlotlyTheme();
  if(!visCo().length||!ratios.length){
    Plotly.react("levelsChart",[],{...theme,title:{text:"Wähle Unternehmen und Kennzahlen.",font:{size:13}},
      xaxis:{visible:false},yaxis:{visible:false},margin:{t:50}},{responsive:true});return;
  }
  const traces=[];
  visCo().forEach(sc=>{
    ratios.forEach((ratio,ri)=>{
      const lv=LEVELS[sc.ticker]?.[ratio];
      if(!lv)return;
      let yvals=lv.values;
      let yTitle="Wert";
      if(lvMode==="delta"){
        yvals=lv.values.map((v,i)=>i===0?null:v-lv.values[i-1]);
        yTitle="ΔWert";
      } else if(lvMode==="norm"){
        const mean=lv.values.reduce((a,b)=>a+b,0)/lv.values.length;
        const std=Math.sqrt(lv.values.reduce((a,b)=>a+(b-mean)**2,0)/lv.values.length);
        yvals=std>0?lv.values.map(v=>(v-mean)/std):lv.values;
        yTitle="z-Score";
      }
      const cNl=COMP[sc.ticker]?.name||sc.ticker;
      traces.push({x:lv.quarters,y:yvals,name:cNl+" · "+(RL[ratio]||ratio),type:"scatter",mode:"lines",
        line:{color:sc.color,width:2,dash:DASHES[ri%DASHES.length]},connectgaps:false,
        hovertemplate:"<b>"+cNl+"</b> "+(RL[ratio]||ratio)+"<br>%{x}: %{y:.4f}<extra></extra>"});
    });
  });
  const tl=ratios.map(r=>RL[r]||r).join(", ");
  const modeLabel=lvMode==="delta"?" (Erste Differenzen)":lvMode==="norm"?" (z-standardisiert)":"";
  Plotly.react("levelsChart",traces,{...theme,
    title:{text:tl+" – Levels"+modeLabel,font:{size:13}},
    xaxis:{...theme.xaxis,title:"Quartal",tickangle:-45},
    yaxis:{...theme.yaxis,title:lvMode==="delta"?"ΔWert":lvMode==="norm"?"z-Score":"Wert"},
    shapes:eventShapes(),annotations:eventAnnotations(),
    legend:{orientation:"h",y:-.18,x:.5,xanchor:"center",font:{size:9}},
    margin:{t:40,r:10,b:70,l:50},hovermode:"x unified"
  },{responsive:true});
}

// ═══════════════════════════════════════════
// TAB 5: ROHDATEN
// ═══════════════════════════════════════════
function updateRawData(){
  const cols=[...rawActiveCols];
  const theme=getPlotlyTheme();
  if(!visCo().length||!cols.length){
    Plotly.react("rawChart",[],{...theme,title:{text:"Wähle Unternehmen und Datenreihen.",font:{size:13}},
      xaxis:{visible:false},yaxis:{visible:false},margin:{t:50}},{responsive:true});return;
  }
  const traces=[];
  visCo().forEach(sc=>{
    cols.forEach((col,ci)=>{
      const rd=RAW[sc.ticker]?.[col];
      if(!rd)return;
      let yvals=rd.values;let yTitle="$";
      if(rawMode==="growth"){
        yvals=rd.values.map((v,i)=>i===0||rd.values[i-1]===0?null:(v-rd.values[i-1])/Math.abs(rd.values[i-1])*100);
        yTitle="Q/Q %";
      } else if(rawMode==="index"){
        const base=rd.values.find(v=>v!=null&&v!==0);
        yvals=base?rd.values.map(v=>v!=null?v/base*100:null):rd.values;
        yTitle="Index (Start=100)";
      }
      const cNr=COMP[sc.ticker]?.name||sc.ticker;
      traces.push({x:rd.quarters,y:yvals,name:cNr+" · "+(RAW_LABELS[col]||col),type:"scatter",mode:"lines",
        line:{color:sc.color,width:2,dash:DASHES[ci%DASHES.length]},connectgaps:false,
        hovertemplate:"<b>"+cNr+"</b> "+(RAW_LABELS[col]||col)+"<br>%{x}: %{y:,.0f}<extra></extra>"});
    });
  });
  const tl=cols.map(c=>RAW_LABELS[c]||c).join(", ");
  const modeLabel=rawMode==="growth"?" (Q/Q %)":rawMode==="index"?" (Index=100)":"";
  Plotly.react("rawChart",traces,{...theme,
    title:{text:tl+modeLabel,font:{size:13}},
    xaxis:{...theme.xaxis,title:"Quartal",tickangle:-45},yaxis:{...theme.yaxis,title:rawMode==="growth"?"Q/Q %":rawMode==="index"?"Index":"$"},
    shapes:eventShapes(),annotations:eventAnnotations(),
    legend:{orientation:"h",y:-.18,x:.5,xanchor:"center",font:{size:9}},
    margin:{t:40,r:10,b:70,l:55},hovermode:"x unified"
  },{responsive:true});
}

// ═══════════════════════════════════════════
// TAB 6: INTERDEPENDENZ
// ═══════════════════════════════════════════
function updateInterdependence(){
  const view=document.getElementById("idView").value;
  const theme=getPlotlyTheme();

  if(view==="heatmap_phi1"||view==="heatmap_sigma"){
    const data=view==="heatmap_phi1"?INTER.phi1_corr:INTER.sigma_corr;
    const pdata=view==="heatmap_phi1"?INTER.pval_phi1:INTER.pval_sigma;
    const labels=data.labels.map(r=>RL[r]||r);
    // Add significance markers
    const textMat=data.matrix.map((row,i)=>row.map((v,j)=>{
      const p=pdata.matrix[i]?.[j];
      const sig=p!=null&&p<0.05?"*":"";
      return v!=null?v.toFixed(3)+sig:"";
    }));
    const trace={
      z:data.matrix,x:labels,y:labels,type:"heatmap",
      colorscale:[[0,"#1565c0"],[0.5,"#fff"],[1,"#c62828"]],
      zmin:-1,zmax:1,showscale:true,
      hovertemplate:"%{y} × %{x}: %{z:.3f}<extra></extra>"
    };
    // Block structure lines (Profitabilität: 0-3, Liquidität: 4, Kapitalstruktur: 5-6)
    const blockShapes=[
      {type:"rect",x0:-.5,x1:3.5,y0:-.5,y1:3.5,line:{color:"#333",width:2},fillcolor:"transparent"},
      {type:"rect",x0:3.5,x1:4.5,y0:3.5,y1:4.5,line:{color:"#333",width:2},fillcolor:"transparent"},
      {type:"rect",x0:4.5,x1:6.5,y0:4.5,y1:6.5,line:{color:"#333",width:2},fillcolor:"transparent"}
    ];
    // Annotations only (no texttemplate to avoid overlap)
    const annots=data.matrix.flatMap((row,i)=>row.map((v,j)=>{
      const p=pdata.matrix[i]?.[j];
      const sig=p!=null&&p<0.05?"*":"";
      return {
        x:labels[j],y:labels[i],text:v!=null?v.toFixed(2)+sig:"",showarrow:false,
        font:{size:10,color:Math.abs(v||0)>0.4?"white":"#333"}
      };
    }));
    Plotly.react("interdepChart",[trace],{...theme,
      title:{text:(view==="heatmap_phi1"?"φ₁":"σ")+" Spearman-Korrelation (Drei-Schichten-Blockstruktur)",font:{size:13}},
      shapes:blockShapes,
      xaxis:{...theme.xaxis,tickangle:-45},yaxis:{...theme.yaxis,autorange:"reversed"},
      margin:{t:45,r:10,b:80,l:90},
      annotations:annots
    },{responsive:true});
  } else if(view==="cramers"){
    // Build 7x7 matrix from cramers pairs
    const labels=RATIOS.map(r=>RL[r]||r);
    const mat=Array.from({length:7},()=>Array(7).fill(0));
    INTER.cramers.forEach(c=>{
      const i=RATIOS.indexOf(c.ratio_a);
      const j=RATIOS.indexOf(c.ratio_b);
      if(i>=0&&j>=0){mat[i][j]=c.cramers_v;mat[j][i]=c.cramers_v;}
    });
    for(let i=0;i<7;i++)mat[i][i]=1;
    const trace={z:mat,x:labels,y:labels,type:"heatmap",
      colorscale:[[0,"#fff3e0"],[0.3,"#ff9800"],[0.6,"#e65100"],[1,"#b71c1c"]],
      zmin:0,zmax:1,hovertemplate:"%{y} × %{x}: V=%{z:.3f}<extra></extra>"};
    const blockShapes=[
      {type:"rect",x0:-.5,x1:3.5,y0:-.5,y1:3.5,line:{color:"#333",width:2},fillcolor:"transparent"},
      {type:"rect",x0:3.5,x1:4.5,y0:3.5,y1:4.5,line:{color:"#333",width:2},fillcolor:"transparent"},
      {type:"rect",x0:4.5,x1:6.5,y0:4.5,y1:6.5,line:{color:"#333",width:2},fillcolor:"transparent"}
    ];
    Plotly.react("interdepChart",[trace],{...theme,
      title:{text:"Cramér's V – Quadrant-Überschneidung",font:{size:13}},
      shapes:blockShapes,
      xaxis:{...theme.xaxis,tickangle:-45},yaxis:{...theme.yaxis,autorange:"reversed"},
      margin:{t:45,r:10,b:80,l:90},
      annotations:mat.flatMap((row,i)=>row.map((v,j)=>({
        x:labels[j],y:labels[i],text:v.toFixed(2),showarrow:false,
        font:{size:10,color:v>0.3?"white":"#333"}
      })))
    },{responsive:true});
  }
}

// ═══════════════════════════════════════════
// TAB 7: VALIDIERUNG
// ═══════════════════════════════════════════
function updateValidation(){
  const view=document.getElementById("valView").value;
  const theme=getPlotlyTheme();

  // Show/hide controls
  document.getElementById("valSizeCtrl").style.display=view==="size"?"":"none";
  document.getElementById("valTargetCtrl").style.display=view==="size"?"":"none";
  document.getElementById("valRatioCtrl").style.display=(view==="size"||view==="kmeans")?"":"none";

  if(view==="chi2"){
    const sorted=[...VAL.chi2].sort((a,b)=>b.cramers_v-a.cramers_v);
    const trace={
      x:sorted.map(r=>RL[r.ratio]||r.ratio),y:sorted.map(r=>r.cramers_v),
      type:"bar",marker:{color:sorted.map(r=>r.significant?"#1565c0":"#ccc")},
      text:sorted.map(r=>"V="+r.cramers_v.toFixed(3)+(r.significant?" ***":"")),textposition:"outside",
      hovertemplate:"%{x}<br>Cramér's V: %{y:.3f}<br>χ²: "+sorted.map(r=>r.chi2).join(",")+("<extra></extra>")
    };
    // Add sector-quadrant distribution as secondary chart
    Plotly.react("validationChart",[trace],{...theme,
      title:{text:"χ²-Test: Sektor-Quadrant-Assoziation (Cramér's V)",font:{size:13}},
      xaxis:{...theme.xaxis},yaxis:{...theme.yaxis,title:"Cramér's V",range:[0,0.35]},
      margin:{t:45,r:10,b:40,l:50},
      shapes:[{type:"line",x0:-.5,x1:6.5,y0:0.1,y1:0.1,line:{color:"#999",dash:"dash",width:1}},
              {type:"line",x0:-.5,x1:6.5,y0:0.3,y1:0.3,line:{color:"#999",dash:"dash",width:1}}],
      annotations:[{x:6.5,y:0.1,text:"schwach",showarrow:false,font:{size:8,color:"#999"}},
                   {x:6.5,y:0.3,text:"mittel",showarrow:false,font:{size:8,color:"#999"}}]
    },{responsive:true});
  } else if(view==="size"){
    const ratio=document.getElementById("valRatio").value||RATIOS[0];
    const sizeVar=document.getElementById("valSizeVar").value;
    const target=document.getElementById("valTarget").value;
    const xvals=[],yvals=[],texts=[];
    tickers.forEach(t=>{
      const c=COMP[t];
      const xv=sizeVar==="market_cap"?c.market_cap:c.employees;
      const yv=target==="phi1"?c.phi1[ratio]:c.sigma[ratio];
      if(xv!=null&&xv>0&&yv!=null){
        xvals.push(Math.log10(xv));yvals.push(yv);texts.push(t);
      }
    });
    // Find matching size_effect
    const eff=VAL.size_effects.find(e=>e.ratio===ratio&&e.size_var===sizeVar&&e.target===target);
    const rhoText=eff?`ρ=${eff.rho} (p=${eff.p!=null?eff.p.toExponential(2):"?"})${eff.significant?" ***":""}`:"";
    const trace={x:xvals,y:yvals,text:texts,type:"scatter",mode:"markers",
      marker:{color:"#1565c0",size:4,opacity:.5},
      hovertemplate:'<b>%{text}</b><br>log₁₀('+(sizeVar==='market_cap'?'MCap':'Empl.')+'):%{x:.2f}<br>'+(target==='phi1'?'φ₁':'σ')+':%{y:.4f}<extra></extra>'};
    const sizeLabel=sizeVar==='market_cap'?'Marktkapitalisierung':'Mitarbeiter';
    const targetLabel=target==='phi1'?'φ₁':'σ';
    Plotly.react("validationChart",[trace],{...theme,
      title:{text:(RL[ratio]||ratio)+' – '+sizeLabel+' vs '+targetLabel+'  '+rhoText,font:{size:12}},
      xaxis:{...theme.xaxis,title:'log₁₀('+(sizeVar==='market_cap'?'MarketCap $':'Mitarbeiter')+')'},
      yaxis:{...theme.yaxis,title:target==='phi1'?'φ₁':'σ(ΔY)'},
      margin:{t:45,r:10,b:50,l:55}
    },{responsive:true});
  } else if(view==="consistency"){
    const scores=VAL.company_consistency.map(c=>c.score);
    const trace={x:scores,type:"histogram",nbinsx:20,marker:{color:"#1565c0",line:{color:"#0d47a1",width:1}},
      hovertemplate:"Score: %{x:.2f}<br>Anzahl: %{y}<extra></extra>"};
    const cons=VAL.consistency["Gesamt (7 Ratios)"]||{};
    Plotly.react("validationChart",[trace],{...theme,
      title:{text:"Konsistenz-Score Verteilung (Ø="+fmt(cons.mean,2)+", Median="+fmt(cons.median,2)+", "+fmt(cons.pct_fully,1)+"% voll konsistent)",font:{size:12}},
      xaxis:{...theme.xaxis,title:"Konsistenz-Score (Anteil gleicher Quadrant)",dtick:0.1},
      yaxis:{...theme.yaxis,title:"Anzahl Unternehmen"},
      margin:{t:45,r:10,b:50,l:50},
      shapes:[{type:"line",x0:cons.mean||0,x1:cons.mean||0,y0:0,y1:1,yref:"paper",line:{color:"#c62828",dash:"dash",width:2}}]
    },{responsive:true});
  } else if(view==="kmeans"){
    const ratio=document.getElementById("valRatio").value||RATIOS[0];
    const traces=[{},{}];// cluster 0 and 1
    [0,1].forEach(cl=>{
      const pts=tickers.filter(t=>COMP[t].kmeans===cl&&COMP[t].phi1[ratio]!=null);
      traces[cl]={
        x:pts.map(t=>COMP[t].phi1[ratio]),y:pts.map(t=>COMP[t].sigma[ratio]),
        text:pts,name:"Cluster "+cl+" (n="+pts.length+")",type:"scatter",mode:"markers",
        marker:{color:cl===0?"#1565c0":"#c62828",size:5,opacity:.6},
        hovertemplate:"<b>%{text}</b><br>φ₁: %{x:.4f}<br>σ: %{y:.4f}<extra>Cluster "+cl+"</extra>"
      };
    });
    Plotly.react("validationChart",traces,{...theme,
      title:{text:(RL[ratio]||ratio)+" – K-Means Cluster (k=2)",font:{size:13}},
      xaxis:{...theme.xaxis,title:"φ₁"},yaxis:{...theme.yaxis,title:"σ(ΔY)"},
      margin:{t:40,r:10,b:50,l:55},legend:{orientation:"h",y:-.12,x:.5,xanchor:"center"}
    },{responsive:true});
  }
}

// ═══════════════════════════════════════════
// TAB 8: ROBUSTHEIT
// ═══════════════════════════════════════════
function updateRobustness(){
  const view=document.getElementById("robView").value;
  const theme=getPlotlyTheme();

  if(view==="sample"){
    // Group by sample, show phi1_median per ratio
    const samples=[...new Set(ROB.sample_comparison.map(r=>r.sample))];
    const traces=samples.map((s,si)=>{
      const rows=ROB.sample_comparison.filter(r=>r.sample===s);
      return {
        x:rows.map(r=>RL[r.ratio]||r.ratio),y:rows.map(r=>r.phi1_median),
        name:s+" (n="+rows[0]?.n+")",type:"bar",
        marker:{color:PALETTE[si%PALETTE.length]}
      };
    });
    Plotly.react("robustnessChart",traces,{...theme,barmode:"group",
      title:{text:"φ₁-Mediane nach Sample-Kriterium",font:{size:13}},
      xaxis:{...theme.xaxis},yaxis:{...theme.yaxis,title:"φ₁ Median"},
      margin:{t:40,r:10,b:40,l:50},legend:{orientation:"h",y:-.12,x:.5,xanchor:"center",font:{size:9}}
    },{responsive:true});
  } else if(view==="finserv"){
    // Financial services medians vs main sample
    const mainRows=ROB.sample_comparison.filter(r=>r.sample.includes("Haupt"));
    const fsKeys=Object.keys(ROB.fs_medians).filter(k=>k!=="");
    const traces=[{
      x:mainRows.map(r=>RL[r.ratio]||r.ratio),y:mainRows.map(r=>r.phi1_median),
      name:"Hauptstichprobe",type:"bar",marker:{color:"#1565c0"}
    }];
    fsKeys.forEach((s,si)=>{
      const med=ROB.fs_medians[s];
      traces.push({
        x:RATIOS.map(r=>RL[r]||r),y:RATIOS.map(r=>med[r]||null),
        name:s,type:"bar",marker:{color:PALETTE[(si+2)%PALETTE.length]}
      });
    });
    Plotly.react("robustnessChart",traces,{...theme,barmode:"group",
      title:{text:"φ₁-Mediane: Hauptstichprobe vs Financial Services",font:{size:13}},
      xaxis:{...theme.xaxis},yaxis:{...theme.yaxis,title:"φ₁ Median"},
      margin:{t:40,r:10,b:40,l:50},legend:{orientation:"h",y:-.12,x:.5,xanchor:"center",font:{size:9}}
    },{responsive:true});
  } else if(view==="funnel"){
    const sorted=[...ROB.sample_counts].sort((a,b)=>a.min_q-b.min_q);
    const trace={
      x:sorted.map(r=>r.sample),y:sorted.map(r=>r.n_tickers),type:"funnel",
      marker:{color:sorted.map((_,i)=>PALETTE[i%PALETTE.length])},
      textinfo:"value+percent initial",
      hovertemplate:"%{x}<br>Ticker: %{y}<extra></extra>"
    };
    Plotly.react("robustnessChart",[trace],{...theme,
      title:{text:"Stichproben-Trichter: Ticker-Anzahl nach Mindest-Quartalen",font:{size:13}},
      margin:{t:40,r:10,b:40,l:150}
    },{responsive:true});
  }
}

// ═══════════════════════════════════════════
// URL HASH NAVIGATION
// ═══════════════════════════════════════════
function updateHash(){
  const parts=["tab="+activeTab];
  if(selectedCompanies.length)parts.push("c="+selectedCompanies.map(c=>c.ticker).join(","));
  const ratio=document.getElementById("ratioSel").value;
  if(ratio)parts.push("r="+ratio);
  history.replaceState(null,"","#"+parts.join("&"));
}

function readHash(){
  const h=location.hash.slice(1);if(!h)return;
  const params={};h.split("&").forEach(p=>{const[k,v]=p.split("=");if(k&&v)params[k]=v;});
  if(params.tab){
    const btn=document.querySelector(`.tab-btn[data-tab="${params.tab}"]`);
    if(btn)btn.click();
  }
  if(params.c){params.c.split(",").forEach(t=>{if(COMP[t])addCompany(t);});}
  if(params.r){document.getElementById("ratioSel").value=params.r;}
}

// ═══════════════════════════════════════════
// DARK MODE
// ═══════════════════════════════════════════
document.getElementById("darkBtn").addEventListener("click",()=>{
  darkMode=!darkMode;
  document.documentElement.setAttribute("data-theme",darkMode?"dark":"");
  document.getElementById("darkBtn").textContent=darkMode?"☀️":"🌙";
  updateCurrentTab();
});

// ═══════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════
document.getElementById("exportBtn").addEventListener("click",()=>{
  const chartId={scatter:"scatterChart",crossratio:"crossChart",timeline:"timelineChart",
    levels:"levelsChart",rawdata:"rawChart",interdependence:"interdepChart",
    validation:"validationChart",robustness:"robustnessChart"}[activeTab];
  if(chartId)Plotly.downloadImage(chartId,{format:"png",width:1600,height:900,filename:"dynamik_explorer_"+activeTab});
});

document.getElementById("csvExportBtn").addEventListener("click",()=>{
  // Export selected companies data as CSV
  if(!selectedCompanies.length){alert("Bitte erst Unternehmen auswählen.");return;}
  let csv="ticker,ratio,phi1,sigma,quadrant,r2,half_life\\n";
  selectedCompanies.forEach(sc=>{
    const c=COMP[sc.ticker];
    RATIOS.forEach(r=>{
      csv+=`${sc.ticker},${r},${c.phi1[r]||""},${c.sigma[r]||""},${c.quadrants[r]||""},${c.r2?.[r]||""},${c.half_life?.[r]||""}\\n`;
    });
  });
  const blob=new Blob([csv],{type:"text/csv"});
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="dynamik_export.csv";a.click();
});

// ═══════════════════════════════════════════
// GUIDED TOUR
// ═══════════════════════════════════════════
const tourSteps=[
  {title:"Willkommen zum Dynamik-Explorer",text:"Dieses Dashboard visualisiert die Ergebnisse der Masterarbeit 'Zeitreihenbasierte Analyse der Dynamik von Finanzkennzahlen'. 932 S&P 1500 Unternehmen × 7 Kennzahlen × 100 Quartale.",tab:null},
  {title:"Die Vier-Quadranten-Klassifikation",text:"Jedes Unternehmen wird anhand von φ₁ (Persistenz) und σ (Volatilität) in einen von vier Quadranten eingeordnet: Korrektiv-Stabil (blau), Korrektiv-Volatil (orange), Persistent-Stabil (grün), Persistent-Volatil (rot).",tab:"scatter",setup:()=>{document.getElementById("ratioSel").value="ROA";document.getElementById("colorSel").value="quadrant";}},
  {title:"Die Drei-Schichten-Hierarchie",text:"Profitabilitätskennzahlen (ROA, ROE, EBIT-Marge, FCF-Marge) zeigen starke Korrekturtendenzen (φ₁ < −0.4). Liquidität (Current Ratio) ist nahezu random walk. Kapitalstruktur (D/E, EK-Quote) zeigt schwache Persistenz.",tab:"crossratio",setup:()=>{document.getElementById("crMetric").value="phi1";}},
  {title:"Blockstruktur der Interdependenz",text:"Die Spearman-Korrelationsmatrix zeigt drei klar abgegrenzte Blöcke: Innerhalb der Profitabilitätskennzahlen sind φ₁-Werte hoch korreliert (ρ > 0.5), zwischen den Schichten nur schwach.",tab:"interdependence",setup:()=>{document.getElementById("idView").value="heatmap_phi1";}},
  {title:"Cramér's V bestätigt die Blockstruktur",text:"Die Quadrant-Überschneidung (Cramér's V) zeigt: ROA↔ROE hat V=0.60 – wer bei ROA korrektiv ist, ist es meist auch bei ROE. Zwischen den Schichten fallen die V-Werte deutlich ab.",tab:"interdependence",setup:()=>{document.getElementById("idView").value="cramers";}},
  {title:"Sektoren bestimmen die Dynamik",text:"Der χ²-Test zeigt signifikante Assoziation zwischen Sektor und Quadrant-Zugehörigkeit. Die stärksten Effekte finden sich bei EBIT-Marge und FCF-Marge (V ≈ 0.28).",tab:"validation",setup:()=>{document.getElementById("valView").value="chi2";}},
  {title:"Größe beeinflusst Volatilität, nicht Persistenz",text:"Die Spearman-Korrelation zeigt: Unternehmensgröße (MarketCap) korreliert negativ mit σ (größere Firmen sind stabiler), aber kaum mit φ₁. Persistenz ist also größenunabhängig.",tab:"validation",setup:()=>{document.getElementById("valView").value="size";}},
  {title:"Robuste Ergebnisse",text:"Die φ₁-Mediane sind über verschiedene Stichprobenkriterien (40Q–100Q) und auch für Financial Services (die in der Hauptstichprobe ausgeschlossen sind) bemerkenswert stabil.",tab:"robustness",setup:()=>{document.getElementById("robView").value="sample";}},
  {title:"Jetzt frei explorieren!",text:"Nutze die Suche (rechts) um einzelne Unternehmen auszuwählen und über alle Tabs hinweg zu vergleichen. Die Auswahl bleibt global erhalten. Viel Spaß beim Entdecken!",tab:null}
];
let tourIdx=0;

function showTourStep(){
  const step=tourSteps[tourIdx];
  document.getElementById("tourProgress").textContent=`Schritt ${tourIdx+1} von ${tourSteps.length}`;
  document.getElementById("tourTitle").textContent=step.title;
  document.getElementById("tourText").textContent=step.text;
  document.getElementById("tourPrev").style.display=tourIdx>0?"":"none";
  document.getElementById("tourNext").textContent=tourIdx<tourSteps.length-1?"Weiter →":"Fertig ✓";
  if(step.tab){
    const btn=document.querySelector(`.tab-btn[data-tab="${step.tab}"]`);
    if(btn){btn.click();}
    if(step.setup)setTimeout(step.setup,100);
    setTimeout(updateCurrentTab,200);
  }
}

document.getElementById("tourBtn").addEventListener("click",()=>{
  tourIdx=0;document.getElementById("tourOverlay").classList.add("active");showTourStep();
});
document.getElementById("tourSkip").addEventListener("click",()=>{
  document.getElementById("tourOverlay").classList.remove("active");
});
document.getElementById("tourNext").addEventListener("click",()=>{
  if(tourIdx<tourSteps.length-1){tourIdx++;showTourStep();}
  else document.getElementById("tourOverlay").classList.remove("active");
});
document.getElementById("tourPrev").addEventListener("click",()=>{
  if(tourIdx>0){tourIdx--;showTourStep();}
});

// ═══════════════════════════════════════════
// COMPARE MODE
// ═══════════════════════════════════════════
document.getElementById("compareBtn").addEventListener("click",()=>{
  if(selectedCompanies.length<2){alert("Bitte mindestens 2 Unternehmen auswählen.");return;}
  // Simple: just highlight that both are in the charts
  alert("Vergleichsmodus: "+selectedCompanies[0].ticker+" vs "+selectedCompanies[1].ticker+"\\nBeide Unternehmen sind in allen Charts hervorgehoben.");
});

// ═══════════════════════════════════════════
// INIT: Populate controls
// ═══════════════════════════════════════════
// Scatter ratio dropdown
const rSel=document.getElementById("ratioSel");
RATIOS.forEach(r=>{const o=document.createElement("option");o.value=r;o.textContent=RL[r]||r;rSel.appendChild(o);});
["ratioSel","xSel","ySel","colorSel"].forEach(id=>document.getElementById(id).addEventListener("change",()=>{renderSectorBar();updateScatter();}));

// Cluster overlay toggle
document.getElementById("clusterOverlay").addEventListener("click",function(){this.classList.toggle("active");updateScatter();});

// Cross-ratio controls
["crView","crMetric"].forEach(id=>document.getElementById(id).addEventListener("change",updateCrossRatio));
// Profile scatter controls
["crLayerAll","crLayerSplit"].forEach(id=>{
  document.getElementById(id).addEventListener("click",function(){
    ["crLayerAll","crLayerSplit"].forEach(i=>document.getElementById(i).classList.remove("active"));
    this.classList.add("active");
    crLayerMode=id==="crLayerAll"?"all":"split";
    updateCrossRatio();
  });
});
// Fixed axis toggle
["crAxisDynamic","crAxisFixed"].forEach(id=>{
  document.getElementById(id).addEventListener("click",function(){
    ["crAxisDynamic","crAxisFixed"].forEach(i=>document.getElementById(i).classList.remove("active"));
    this.classList.add("active");
    crFixedAxes=id==="crAxisFixed";
    updateCrossRatio();
  });
});
// Benchmark select: dynamically populate with sectors of selected companies
function updateBenchSelect(){
  const sel=document.getElementById("crBenchSelect");
  const prev=new Set([...sel.selectedOptions].map(o=>o.value));
  sel.innerHTML='<option value="global">Gesamt-Median (932)</option>';
  // Add sector options based on ALL available sectors
  const sectors=[...allSectors].sort();
  sectors.forEach(s=>{
    const o=document.createElement("option");o.value="sector:"+s;
    const sm=D.sector_medians[s];
    const n=sm?sm[RATIOS[0]]?.n||'?':'?';
    o.textContent='Ø '+s+' ('+n+')';
    sel.appendChild(o);
  });
  // Restore previous selection
  [...sel.options].forEach(o=>{if(prev.has(o.value))o.selected=true;});
  // Auto-select sectors of current companies
  const currentSectors=new Set(selectedCompanies.map(sc=>COMP[sc.ticker]?.sector).filter(Boolean));
  currentSectors.forEach(s=>{
    const opt=[...sel.options].find(o=>o.value==="sector:"+s);
    if(opt&&!prev.size)opt.selected=true;// only auto-select if nothing was selected before
  });
}
document.getElementById("crBenchSelect").addEventListener("change",updateCrossRatio);

// AR order counter
document.getElementById("arUp").addEventListener("click",()=>{if(arOrder<5){arOrder++;document.getElementById("arVal").textContent=arOrder;updateTimeline();}});
document.getElementById("arDown").addEventListener("click",()=>{if(arOrder>1){arOrder--;document.getElementById("arVal").textContent=arOrder;updateTimeline();}});
document.getElementById("tlMetric").addEventListener("change",updateTimeline);

// Timeline toggles
["tlConfBand","tlMedian","tlAllPhi"].forEach(id=>{
  document.getElementById(id).addEventListener("click",function(){this.classList.toggle("active");updateTimeline();});
});

// Timeline ratio checkboxes
const tlActiveRatios=new Set([RATIOS[0]]);
const tlC=document.getElementById("tlRatioChecks");
RATIOS.forEach(r=>{
  const l=document.createElement("label");l.className=tlActiveRatios.has(r)?"active":"";
  const cb=document.createElement("input");cb.type="checkbox";cb.checked=tlActiveRatios.has(r);
  l.appendChild(cb);l.appendChild(document.createTextNode(RL[r]||r));
  l.addEventListener("click",e=>{e.preventDefault();if(tlActiveRatios.has(r)){tlActiveRatios.delete(r);cb.checked=false;l.classList.remove("active");}else{tlActiveRatios.add(r);cb.checked=true;l.classList.add("active");}updateTimeline();});
  tlC.appendChild(l);
});

// Levels ratio checkboxes
const lvActiveRatios=new Set([RATIOS[0]]);
const lvC=document.getElementById("lvRatioChecks");
RATIOS.forEach(r=>{
  const l=document.createElement("label");l.className=lvActiveRatios.has(r)?"active":"";
  const cb=document.createElement("input");cb.type="checkbox";cb.checked=lvActiveRatios.has(r);
  l.appendChild(cb);l.appendChild(document.createTextNode(RL[r]||r));
  l.addEventListener("click",e=>{e.preventDefault();if(lvActiveRatios.has(r)){lvActiveRatios.delete(r);cb.checked=false;l.classList.remove("active");}else{lvActiveRatios.add(r);cb.checked=true;l.classList.add("active");}updateLevels();});
  lvC.appendChild(l);
});

// Levels mode toggles
["lvLevels","lvDelta","lvNorm"].forEach(id=>{
  document.getElementById(id).addEventListener("click",function(){
    ["lvLevels","lvDelta","lvNorm"].forEach(i=>document.getElementById(i).classList.remove("active"));
    this.classList.add("active");
    lvMode={lvLevels:"levels",lvDelta:"delta",lvNorm:"norm"}[id];
    updateLevels();
  });
});

// Raw data checkboxes
const rawCols=Object.keys(RAW_LABELS);
const rawActiveCols=new Set([rawCols[0]]);
const rawC=document.getElementById("rawChecks");
rawCols.forEach(col=>{
  const l=document.createElement("label");l.className=rawActiveCols.has(col)?"active":"";
  const cb=document.createElement("input");cb.type="checkbox";cb.checked=rawActiveCols.has(col);
  l.appendChild(cb);l.appendChild(document.createTextNode(RAW_LABELS[col]||col));
  l.addEventListener("click",e=>{e.preventDefault();if(rawActiveCols.has(col)){rawActiveCols.delete(col);cb.checked=false;l.classList.remove("active");}else{rawActiveCols.add(col);cb.checked=true;l.classList.add("active");}updateRawData();});
  rawC.appendChild(l);
});

// Raw mode toggles
["rawAbs","rawGrowth","rawIndex"].forEach(id=>{
  document.getElementById(id).addEventListener("click",function(){
    ["rawAbs","rawGrowth","rawIndex"].forEach(i=>document.getElementById(i).classList.remove("active"));
    this.classList.add("active");
    rawMode={rawAbs:"abs",rawGrowth:"growth",rawIndex:"index"}[id];
    updateRawData();
  });
});

// Interdependence controls
document.getElementById("idView").addEventListener("change",updateInterdependence);

// Validation controls
const valRSel=document.getElementById("valRatio");
RATIOS.forEach(r=>{const o=document.createElement("option");o.value=r;o.textContent=RL[r]||r;valRSel.appendChild(o);});
["valView","valRatio","valSizeVar","valTarget"].forEach(id=>document.getElementById(id).addEventListener("change",updateValidation));

// Robustness controls
document.getElementById("robView").addEventListener("change",updateRobustness);

// ═══════════════════════════════════════════
// BOOT
// ═══════════════════════════════════════════
renderSectorBar();
renderSidebar();
updateBenchSelect();
renderCrSectorBar();
updateScatter();
readHash();
</script>
</body>
</html>'''

# Inject data into template
html = html_template.replace('__DATA_JSON__', data_json)

# Write output
out_path = BASE / "dynamik_explorer.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ Dashboard written to {out_path}")
print(f"   File size: {os.path.getsize(out_path)/1024/1024:.1f} MB")
print(f"   Open in browser to verify.")
