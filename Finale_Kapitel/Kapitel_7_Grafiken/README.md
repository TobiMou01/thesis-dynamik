# Chapter 7 Graphics - Externe Validierung (FF3)

All 5 publication-quality graphics for the external validation chapter have been successfully created.

## Graphics Summary

### 1. abb_7_1_chi2_cramers_v.png (107 KB)
**Cramér's V Effect Sizes from χ² Tests**
- Horizontal bar chart showing association strength between sectors and quadrants
- 7 financial ratios sorted by descending effect size
- Color-coded by category: blue (profitability), orange (liquidity), green (capital structure)
- Reference lines indicating small (0.1) and medium (0.3) effect thresholds
- Values range: 0.176 (D/E) to 0.286 (Current Ratio)

### 2. abb_7_2_groesseneffekte.png (113 KB)
**Size Effects on Volatility and Persistence**
- Two-panel figure (side-by-side design)
- **Left:** Spearman ρ correlations between firm size (employees) and volatility (σ)
  - All negative correlations indicating size reduces volatility
  - Range: -0.53 (FCF, CR) to -0.01 (D/E)
  - Significance markers (* for p<0.05)
- **Right:** Spearman ρ correlations between size and persistence (φ₁)
  - Correlations near zero indicating minimal size effect on persistence
  - Range: -0.09 (FCF) to +0.10 (D/E)
  - 4 ratios show statistical significance

### 3. abb_7_3_konsistenz.png (81 KB)
**Consistency of Quadrant Classifications**
- Grouped bar chart comparing two consistency metrics across three aggregation levels
- **Levels:** Gesamt (7 ratios), Profitabilität (4 ratios), Kapitalstruktur (2 ratios)
- **Metrics:** Full consistency (dark) vs. Majority ≥50% (light)
- Shows dramatic improvement from 1.2% to 41.5% fully consistent classifications
- Clear evidence of stronger consistency at more specific aggregation levels

### 4. abb_7_4_kmeans_cluster.png (515 KB)
- **Two-panel scatter plot showing K-means clustering results**
- **Left panel:** ROA ratio dynamics
- **Right panel:** D/E ratio dynamics
- Both panels plot persistence (φ₁) vs. volatility (σ)
- Color coding: Cluster 0 (blue, "Stabil") n=751 vs. Cluster 1 (red, "Hochvolatil") n=180
- Cluster centroids marked with black stars
- Shows dramatic volatility differences between clusters, especially for D/E

### 5. abb_7_5_finserv_vergleich.png (110 KB)
**Robustness Check: Main Analysis vs. Financial Services**
- Grouped bar chart comparing median φ₁ (persistence) across 7 ratios
- Dark colors = Main analysis (n=932), Light colors = Financial Services (n=176)
- Highlights dramatic differences for Current Ratio (-0.17 vs -0.41) and D/E (-0.09 vs -0.20)
- Demonstrates that Financial Services sector exhibits different persistence patterns
- Important robustness validation showing sector-specific effects

## Technical Specifications

- **Format:** PNG, 200 DPI (publication quality)
- **Font:** DejaVu Sans, 10-11 pt (academic standard)
- **Style:** Clean white background, minimal gridlines, black axis frames
- **Layout:** Tight layout with no excess whitespace
- **Colors:** Consistent color scheme across all graphics
  - Profitability ratios: Blues (#3182bd)
  - Liquidity ratios: Orange (#ff7f0e)
  - Capital structure ratios: Greens (#2ca02c)

## Integration Notes

All graphics are optimized for thesis publication with German labels and proper statistical notation:
- φ₁ for persistence coefficient
- σ for volatility measure
- Cramér's V for effect size
- Spearman ρ for rank correlations
- n values for sample sizes
- * symbols for statistical significance (p<0.05)

These files are ready for direct integration into the thesis manuscript.
