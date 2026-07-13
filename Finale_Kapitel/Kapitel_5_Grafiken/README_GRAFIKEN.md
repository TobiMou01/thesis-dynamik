# Chapter 5: Financial Ratio Dynamics - Publication Graphics

## Overview
Six high-quality academic graphics created for Chapter 5 of the master's thesis. All graphics follow a consistent design with German labels, academic styling, and a unified color scheme representing three financial ratio categories.

---

## Color Scheme

### Profitabilität (Profitability) - Blues
- ROA: #2171b5
- ROE: #4292c6
- EBIT_margin: #6baed6
- fcf_margin: #9ecae1

### Liquidität (Liquidity) - Orange
- current_ratio: #e6550d

### Kapitalstruktur (Capital Structure) - Greens
- debt_to_equity: #31a354
- equity_ratio: #74c476

### Quadrant Classification
- Korrektiv-Stabil (Corrective-Stable): #2171b5
- Korrektiv-Volatil (Corrective-Volatile): #6baed6
- Persistent-Stabil (Persistent-Stable): #fd8d3c
- Persistent-Volatil (Persistent-Volatile): #e6550d

---

## Graphics

### 1. abb_5_1_drei_schichten_boxplots.png
**Title:** Three-Layer Hierarchy Boxplots

**Description:**
Horizontal boxplot showing the distribution of autoregressive coefficients (φ₁) for all 7 financial ratios, organized by their functional categories (Profitabilität, Liquidität, Kapitalstruktur).

**Key Features:**
- Displays median, quartiles, and outliers for each ratio
- Three-layer categorical structure with visual distinction
- Reference line at φ₁ = 0
- Color-coded by category
- Category labels with background shading

**Interpretation:**
Shows the central tendency and variability of mean reversion across ratios. Profitability ratios exhibit stronger (more negative) mean reversion than capital structure ratios, indicating fundamental differences in their dynamic behavior.

**Dimensions:** 1580 × 1180 px | DPI: 200

---

### 2. abb_5_2_signifikanz_r2.png
**Title:** Statistical Significance and Model Fit

**Description:**
Dual-panel visualization:
- **Left Panel:** Signifikanzrate (%) - percentage of companies showing statistically significant AR(1) coefficients per ratio
- **Right Panel:** R² Median - median explanatory power of the AR(1) model per ratio

**Data:**
| Ratio | Signif. (%) | R² Median |
|-------|-------------|-----------|
| ROA | 92.2% | 0.187 |
| ROE | 90.0% | 0.182 |
| EBIT_margin | 89.8% | 0.186 |
| fcf_margin | 96.6% | 0.211 |
| current_ratio | 45.6% | 0.032 |
| debt_to_equity | 32.4% | 0.018 |
| equity_ratio | 18.6% | 0.008 |

**Key Features:**
- Horizontal bars with same category colors
- Value labels for exact figures
- Clear contrast between profitability (high) and capital structure (low)
- Grid lines for easy reading

**Interpretation:**
Profitability ratios demonstrate strong mean reversion with high significance rates and good fit. Liquidity and capital structure ratios show weak or absent mean reversion, indicating fundamentally different dynamics.

**Dimensions:** 2779 × 1180 px | DPI: 200

---

### 3. abb_5_3_modellvergleich_tabelle.png
**Title:** Model Variant Comparison Heatmap

**Description:**
Comprehensive heatmap comparing autoregressive coefficients (φ₁) across four different estimation models and all seven financial ratios.

**Model Variants:**
1. **diff1** - First differences (baseline)
2. **levels** - Levels specification
3. **ar2_diff1** - AR(2) in differences
4. **diff4** - Fourth differences

**Data Source:** ar/ar_features_all.csv (grouped by model and ratio, φ₁ median)

**Key Features:**
- Diverging colormap (RdBu_r): negative values = blue, zero = white, positive = red
- Cell values annotated with color-coded text (white on strong values, black on weak)
- Ratios ordered by category
- Models as columns

**Interpretation:**
Demonstrates robustness of negative autoregressive coefficients across different model specifications. Consistency suggests that mean reversion patterns are fundamental, not artifacts of specific estimation choices.

**Dimensions:** 1874 × 979 px | DPI: 200

---

### 4. abb_5_4_stichproben_robustheit.png
**Title:** Robustness Across Sample Sizes

**Description:**
Grouped bar chart showing the stability of autoregressive coefficients (φ₁) across four different minimum sample size requirements.

**Sample Sizes:**
- 100Q (Main Analysis) - 100+ quarterly observations
- 80Q - 80+ quarterly observations
- 60Q - 60+ quarterly observations
- 40Q - 40+ quarterly observations

**Key Ratios Analyzed:**
- ROA (Profitabilität)
- fcf_margin (Profitabilität)
- current_ratio (Liquidität)
- debt_to_equity (Kapitalstruktur)
- equity_ratio (Kapitalstruktur)

**Key Features:**
- Four grouped bars per ratio
- Distinct color for each sample size
- Reference line at φ₁ = 0
- Grid lines for easy value reading

**Interpretation:**
Profitability ratios maintain stable negative φ₁ across all sample sizes, indicating robust mean reversion. Capital structure ratios remain near zero regardless of sample size, confirming their lack of systematic mean reversion.

**Dimensions:** 1979 × 1180 px | DPI: 200

---

### 5. abb_5_5_sektor_heatmap.png
**Title:** Sector-Specific Autoregressive Coefficients

**Description:**
Heatmap of autoregressive coefficients (φ₁) stratified by sector and financial ratio. Shows how financial ratio dynamics vary across different economic sectors.

**Data:**
- **Rows:** Economic sectors (sorted by mean φ₁)
- **Columns:** All 7 financial ratios
- **Values:** Median φ₁ within each sector-ratio combination

**Data Source:** Merged ar/ar_features.csv with company_quadrant_profiles.csv

**Key Features:**
- Diverging colormap highlighting mean reversion (negative/blue) vs. drift (positive/red)
- All sector-ratio combinations annotated with values
- Sectors ordered by magnitude of mean reversion
- Missing values handled gracefully

**Interpretation:**
Sectors vary in their financial ratio dynamics. Some sectors show strong mean reversion across all ratios; others show more heterogeneous patterns. Capital-intensive sectors may differ from service-oriented ones.

**Dimensions:** 2273 × 1580 px | DPI: 200

---

### 6. abb_5_6_sektor_quadranten.png
**Title:** Quadrant Distribution by Sector

**Description:**
Stacked horizontal bar chart showing the relative distribution of ratio quadrants across economic sectors. Quadrants represent combinations of mean reversion strength (Korrektiv vs. Persistent) and volatility (Stabil vs. Volatil).

**Quadrant Definitions:**
- **Korrektiv-Stabil:** Strong mean reversion, low volatility
- **Korrektiv-Volatil:** Strong mean reversion, high volatility
- **Persistent-Stabil:** Weak mean reversion, low volatility
- **Persistent-Volatil:** Weak mean reversion, high volatility

**Data Source:** Merged clustering/quadrant_assignments.csv with company_quadrant_profiles.csv

**Aggregation:** All ratios combined per sector

**Key Features:**
- Stacked bars (100% = 100% of sector-ratio observations)
- Four distinct quadrant colors (consistent with color scheme)
- Sectors sorted by share of stable quadrants
- Value labels within bars showing percentages
- Legend with all four quadrant categories

**Interpretation:**
Shows sectoral variation in the prevalence of mean-reverting vs. drifting dynamics. Sectors with high stable shares demonstrate more predictable financial ratio evolution; volatile-heavy sectors require different analytical approaches.

**Dimensions:** 1979 × 1580 px | DPI: 200

---

## Technical Specifications

### Format & Quality
- **Format:** PNG (portable, lossless compression)
- **Resolution:** 200 DPI (suitable for print and digital publication)
- **Color Space:** 8-bit RGBA
- **Total Size:** ~1.0 MB (6 files combined)

### Design Standards
- **Figure Width:** 7-8 inches (suitable for academic journals)
- **Font Size:** 10-11pt (readable at print size)
- **Background:** Clean white
- **Layout:** Tight layout with minimal whitespace
- **Language:** German labels where natural (Kennzahl, Sektor, Anteil, etc.)
- **Style:** Consistent academic presentation

### Software
- **Created with:** Python 3.10
- **Libraries:** Matplotlib 3.5+, Pandas 1.3+, NumPy 1.21+, Seaborn 0.11+
- **Script:** create_chapter5_graphics.py

---

## Integration Notes

### For Word Document
All graphics are optimized for insertion into Word documents:
- High DPI (200) ensures crisp appearance at any zoom level
- PNG format compatible with all office suites
- Aspect ratios suitable for standard column widths

### Cross-References in Text
Suggested figure references:
- **Abb. 5.1:** Introduction to autoregressive dynamics across ratio categories
- **Abb. 5.2:** Significance and explanatory power comparison
- **Abb. 5.3:** Model robustness discussion
- **Abb. 5.4:** Sample size sensitivity analysis
- **Abb. 5.5:** Sector heterogeneity
- **Abb. 5.6:** Quadrant prevalence by sector

---

## File Locations

**Output Directory:**
```
/sessions/keen-friendly-brahmagupta/mnt/Arbeitsort Master/Text/Finale_Kapitel/Kapitel_5_Grafiken/
```

**Generation Script:**
```
/sessions/keen-friendly-brahmagupta/mnt/Arbeitsort Master/create_chapter5_graphics.py
```

**Source Data Files:**
- `output/ar/ar_features.csv` - Main AR(1) estimation results
- `output/ar/ar_features_all.csv` - Results for all model variants
- `output/robustness/sample_comparison.csv` - Sample size robustness tests
- `output/clustering/quadrant_assignments.csv` - Quadrant classifications
- `output/profiles/company_quadrant_profiles.csv` - Company sector information

---

## Creation Date
April 4, 2026

**Version:** 1.0 (Final)
