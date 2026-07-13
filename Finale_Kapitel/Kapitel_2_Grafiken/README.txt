========================================================================
CHAPTER 2 GRAPHICS - PUBLICATION QUALITY
========================================================================

All 5 graphics have been created with the following specifications:
- DPI: 300 (publication quality for print)
- Format: PNG (lossless compression)
- Layout: tight_layout() applied to all
- German labels throughout
- Color: RGBA 8-bit
- Matplotlib rendering engine: Agg (non-interactive backend)

========================================================================
FILE LISTING
========================================================================

1. abb_2_1_niveaus_vs_differenzen.png (404 KB)
   - Dual subplot figure showing ROA levels vs. first differences
   - Top: ROA time series Y(t) with mean line (~0.024 mean)
   - Bottom: ΔROA differences with zero reference and mean-reversion pattern
   - Data: PG (Procter & Gamble) from ratio_panel.csv
   - Shows moderately volatile levels and oscillating differences
   - German title: "Niveaus vs. erste Differenzen: ROA (Procter & Gamble)"

2. abb_2_2_mean_reversion_konzept.png (349 KB)
   - Conceptual dual-panel illustration (NOT real data - schematic)
   - Left: "Niveaupersistenz" - smooth series with φ₁ ≈ 0,93 (EK-Quote)
   - Right: "Veränderungskorrektur" - zigzag oscillations with φ₁ ≈ −0,43 (ROA)
   - Clean design with synthetic data demonstrating the concepts
   - Shows contrast between persistent levels and mean-reverting changes

3. abb_2_3_quadrantenschema.png (296 KB)
   - 2x2 matrix classification diagram
   - X-axis: σ(ΔY) Volatilität der Veränderungen (low to high)
   - Y-axis: φ₁ Autokorrelation (strong negative to near-zero)
   - Four colored quadrants:
     * Blue (top-left): KORREKTIV-STABIL
     * Red (top-right): KORREKTIV-VOLATIL
     * Green (bottom-left): PERSISTENT-STABIL
     * Orange (bottom-right): PERSISTENT-VOLATIL
   - German descriptions for each quadrant
   - Professional design with rounded rectangles

4. abb_2_4_drei_schichten.png (176 KB)
   - Three-layer hierarchy diagram
   - Layer 1 (Blue): Profitabilität - ROA, ROE, EBIT-M., FCF-M. (φ₁ ≈ −0,43 to −0,46)
   - Layer 2 (Green): Liquidität - Current Ratio (φ₁ ≈ −0,17)
   - Layer 3 (Orange): Kapitalstruktur - D/E, EK-Quote (φ₁ ≈ −0,04 to −0,09)
   - Shows correction intensity gradient from top to bottom
   - Clean horizontal band layout

5. abb_2_5_dupont_zerlegung.png (206 KB)
   - Tree/flow diagram of DuPont decomposition
   - Top: ROE (red)
   - Second level: ROA (blue) and Leverage-Faktor (blue)
   - Third level: Gewinnmarge (green) and Kapitalumschlag (green)
   - Shows mechanical coupling: "ROE und D/E teilen sich den Nenner (Eigenkapital)"
   - Connected with multiplication operators
   - Highlights structural relationships

========================================================================
TECHNICAL DETAILS
========================================================================

All figures created using:
- matplotlib 3.x with Agg backend (non-interactive)
- NumPy for numerical operations
- Pandas for data handling
- matplotlib.gridspec for complex layouts
- FancyBboxPatch and FancyArrowPatch for enhanced visuals

Specifications applied uniformly:
- dpi=300 (all outputs)
- tight_layout() for optimal spacing
- High-quality anti-aliasing (default)
- Consistent color palette across all figures
- Professional typography with appropriate font sizes

========================================================================
USAGE NOTES
========================================================================

1. These graphics are ready for direct inclusion in thesis documents
2. Print quality at standard paper sizes (8.5"x11", A4, etc.)
3. All German labels follow academic conventions for German-language texts
4. Color schemes are print-friendly and distinguish elements clearly
5. File names follow German naming conventions (abb_X_Y format)

Generated: 2026-04-04
Directory: /sessions/keen-friendly-brahmagupta/mnt/Arbeitsort Master/Text/Finale_Kapitel/Kapitel_2_Grafiken/

========================================================================
