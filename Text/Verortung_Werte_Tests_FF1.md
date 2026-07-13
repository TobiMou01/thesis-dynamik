# Verortung — Werte & Tests pro Gliederungspunkt (Kapitel 4 / FF1)

**Stand:** 26.04.2026
**Zweck:** Pro Unterabschnitt 4.x.y eine kompakte Bestandsaufnahme: welche Tabellen/Abbildungen, welche Werte, welche Tests. Mit kurzer Erklärung und Verweis auf die Tiefenerklärung in den beiden Glossaren.

**Verweisformat:**
- *KW §X.Y* = Kennwert-Glossar, Sektion X.Y
- *T §Z* = Test-Glossar, Sektion Z

---

## Kapitel-Einleitung (4)

**Inhalt.** Zwei Hauptparameter eingeführt — keine Tabellen.

**Werte.**
- **φ₁** — AR(1)-Koeffizient als Mean-Reversion-Maß der Veränderungen → *KW §A.1*
- **σ(ΔY)** — Standardabweichung der Quartalsveränderungen → *KW §A.5*

**Tests.** Keine.

---

## 4.1 Analyse nach Kennzahl — Einleitung

**Inhalt.** Methodische Vorbemerkung zur Querschnittsmedianverdichtung.

**Werte.**
- **Median** als Aggregations-Statistik über 932 Firmen → *KW §D.2*

**Tests.** Keine.

---

### 4.1.1 Überblick der Drei Dynamiktypen

**Tabellen / Abbildungen.** Tab. 4.1; Abb. 4.1 (Boxplots φ₁); Abb. 4.1b (KDE φ₁); Abb. 4.2 (Sig.-Rate + R²); Abb. 4.2b (KDE σ).

**Werte.**
- **φ₁ Mittelwert / Median / Standardabweichung** — drei Lagemaße zur Beschreibung der φ₁-Verteilung pro Kennzahl → *KW §A.1, §D.1–D.3*
- **σ(ΔY) Mittelwert / Median / Standardabweichung** — analoge Beschreibung der Volatilitäts-Verteilung → *KW §A.5, §D.1–D.3*
- **Signifikanzrate (Sig. %)** — Anteil der Firmen mit p < 0,05 → *KW §B.3*
- **t½ Q / t½ J** — Halblebensdauer in Quartalen und Jahren als ökonomische Übersetzung von φ₁ → *KW §C.1*
- **R²-Verteilung** — Modellgüte, dargestellt in Abb. 4.2 als Boxplot/KDE → *KW §B.1*

**Tests.**
- **t-Test auf φ₁** — pro Firma, aggregiert zur Sig.-Rate → *T §1*

---

### 4.1.2 Profitabilitätsgruppe

**Tabellen / Abbildungen.** Tab. 4.2a (ROA); Tab. 4.2b (ROE); Tab. 4.2c (EBIT-Marge); Tab. 4.2d (FCF-Marge).

**Werte.**
- **φ₁ Mittelwert / Median / Standardabweichung / IQR / 5.+95. Perzentil** — vollständige Verteilungsbeschreibung pro Kennzahl → *KW §A.1, §D.1–D.5*
- **σ(ΔY) Mittelwert / Median / Standardabweichung / IQR / 5.+95. Perzentil** → *KW §A.5, §D.1–D.5*
- **R² Mittelwert / Median / IQR** — Modellgüte pro Kennzahl → *KW §B.1*
- **Signifikanzrate** — Sig. % pro Kennzahl → *KW §B.3*
- **Spearman-Korrelation ρ_σ ≈ 0,82** zwischen ROE-σ und D/E-σ — als algebraischer Hebel-Vorgriff auf Kap. 5 erwähnt → *KW §E.1, T §2*

**Tests.**
- **t-Test auf φ₁** → *T §1*

---

### 4.1.3 Liquiditätsgruppe

**Tabellen / Abbildungen.** Tab. 4.2e (Current Ratio).

**Werte.** Identisches Set wie 4.1.2, plus eine Beobachtung zur Verteilungsform:
- **φ₁ Mittelwert / Median / Std / IQR / p5+p95** → *KW §A.1, §D.1–D.5*
- **σ(ΔY) Mittelwert / Median / Std / IQR / p5+p95** — Auffällig: σ-Spreizung Faktor 23 zwischen p5 und p95 → *KW §A.5*
- **R²** — sehr niedrig (Median 0,028) — selbst aussagekräftiger Befund → *KW §B.1*
- **Signifikanzrate** 45,6 % → *KW §B.3*

**Tests.**
- **t-Test auf φ₁** → *T §1*

---

### 4.1.4 Kapitalstrukturgruppe

**Tabellen / Abbildungen.** Tab. 4.2f (Debt/Equity); Tab. 4.2g (Eigenkapitalquote).

**Werte.**
- **φ₁ Mittelwert / Median / Std / IQR / p5+p95** — der Median liegt nahe Null; positive p5/p95-Werte zeigen Momentum-Quartil → *KW §A.1, §D.1–D.5, §F.4*
- **σ(ΔY) Mittelwert / Median / Std / IQR / p5+p95** — extreme Rechtsschiefe bei D/E (Faktor ~136 zwischen p5 und p95) → *KW §A.5*
- **R²** — sehr niedrig (Median 0,008–0,018), Nullbefund auf Differenzen → *KW §B.1*
- **Signifikanzrate** 32,4 % bzw. 18,6 % → *KW §B.3*
- **Levels-φ₁** als Vorgriff auf 4.5.1 erwähnt: 0,93 für EK-Quote — komplementäre Lesart → *KW §A.1, §F.4*

**Tests.**
- **t-Test auf φ₁** → *T §1*

---

## 4.2 Analyse nach Branche — Einleitung

**Inhalt.** Zerlegung nach 10 GICS-Sektoren; FS ausgeschlossen.

**Werte.** Keine neuen — verwendet werden die Aggregate aus 4.1 sektoral zerlegt.

**Tests.** Keine.

---

### 4.2.1 Sektorale Übersicht der AR(1)-Kenngrößen

**Tabellen / Abbildungen.** Tab. 4.3 (φ₁-Median Sektor × Kennzahl); Tab. 4.3b (σ-Median Sektor × Kennzahl); Tab. 4.3c (Sig.-Rate Sektor × Kennzahl); Abb. 4.5 (Heatmap φ₁); Abb. 4.7 (Heatmap σ); Abb. 4.8 (Heatmap Sig.).

**Werte.**
- **φ₁-Median pro Sektor × Kennzahl** — Lagemaß auf Sektorebene → *KW §A.1, §D.2*
- **σ(ΔY)-Median pro Sektor × Kennzahl** → *KW §A.5, §D.2*
- **Signifikanzrate pro Sektor × Kennzahl** → *KW §B.3*
- **Sektor-Profile** — narrativ zusammengeführt mit Quadranten-Anteilen (Vorgriff auf 4.2.2)

**Tests.** Keine eigenen — implizit der t-Test pro Firma, aber nicht als Test im Abschnitt selbst.

**Lücke.** Die geplante φ₁-Std-Heatmap (Streuungsdimension auf Sektorebene) fehlt — siehe Abgleich-Dokument, Punkt 5.

---

### 4.2.2 Quadrantenverteilung pro Sektor

**Tabellen / Abbildungen.** Tab. 4.4 (Sektor × dominanter Quadrant); Abb. 4.6 (gestapelte Säulen).

**Werte.**
- **Quadranten-Anteile (%)** pro Sektor und Quadrant → einfache Häufigkeitsverteilung
- **Dominanter Quadrant** pro Firma — Konstrukt aus „der häufigste Quadrant über die 7 Kennzahlen" → ordinale Aggregation, kein Test
- **Drei-Gruppen-Sortierung** der Sektoren (Stabile / Korrektiv-Volatile / Persistent-Volatile) — narrative Klassifikation

**Tests.** Keine eigenen. Der Sektor-Quadrant-χ²-Test sitzt in Kap. 6 (FF3), nicht hier.

---

## 4.3 Interpretation der Ergebnisse — Einleitung

**Inhalt.** Argumentationsbogen Hauptachse + zwei Verstärker.

**Werte / Tests.** Keine neuen — Re-Verwendung der bereits etablierten Größen.

---

### 4.3.1 Interpretation der Rangordnung (Schichthierarchie)

**Werte (re-genutzt).**
- **φ₁** als Strukturparameter (Markt-vs.-Management-Lesart) → *KW §A.1*
- **t½** als Zeitkonstanten-Argument (Verstärker 1: Faktor 15 zwischen oberer und unterer Schicht) → *KW §C.1*
- **Levels-φ₁** als komplementäre Lesart (Verweis auf 4.5.1) → *KW §A.1, §F.4*

**Tests.** Keine.

---

### 4.3.2 Interpretation der sektoralen Heterogenität

**Werte (re-genutzt).**
- **φ₁ pro Sektor** für Utilities, Real Estate, Communication Services, Basic Materials, Technology → *KW §A.1*
- **σ pro Sektor** als Geschäftsmodell-Indikator → *KW §A.5*

**Tests.** Keine.

---

### 4.3.3 Interpretation der Quadrantenzugehörigkeit

**Tabellen / Abbildungen.** Tab. 4.10 (Beispielfirmen Walmart / Boeing / Microsoft / Amazon); Abb. 4.10 (z-standardisierte ROA-Zeitreihen).

**Werte.**
- **φ₁ (Einzelfirma)** für die vier Beispiele — z.B. Walmart −0,69 → *KW §A.1*
- **σ(ΔY) (Einzelfirma)** — z.B. Walmart 0,010 → *KW §A.5*
- **R² (Einzelfirma)** — Walmart 0,48 → *KW §B.1*
- **p-Wert (Einzelfirma)** — Walmart/Boeing/MSFT < 0,001, Amazon 0,010 → *KW §B.2*
- **Consistency-Score** (Vorgriff auf Kap. 6) — Walmart 0,86 → narrativ erwähnt
- **Spearman ρ** der Trennbarkeit (Verweis auf 4.5.3) → *KW §E.1, T §2*

**Tests.**
- **t-Test auf φ₁ (Einzelfirma)** — die vier ausgewiesenen p-Werte → *T §1*

---

## 4.4 Erkenntnisse aus FF1

**Werte (re-genutzt).** Komplettes Set aus 4.1–4.3, kondensiert in drei Befunden:
- φ₁-Mediane (Hierarchie)
- Spearman |ρ| < 0,19 / 0,19–0,24 (Trennbarkeit)
- Sektorale φ₁-Variation (Heterogenität)

**Tests (vorausschauend genannt).**
- **Bonferroni-Korrektur** für die 42 Paartests in der Korrelationsmatrix von Kap. 5 → *T §8*

**Eigene Tests in 4.4.** Keine.

---

## 4.5 Robustheit — Einleitung

**Inhalt.** Vier Robustheitsperspektiven angekündigt.

**Werte / Tests.** Keine neuen.

---

### 4.5.1 Modellvarianten

**Tabellen / Abbildungen.** Tab. 4.5 (φ₁-Mediane in vier Modellvarianten); Abb. 4.3 (Modellvergleich-Heatmap).

**Werte.**
- **φ₁-Median** unter den vier Spezifikationen: levels, diff1, AR(2)-diff1, Δ₄Y → *KW §A.1*
- **φ₂** (zweiter Lag in AR(2)-Spezifikation) → *KW §A.2*
- **R²-Median** im Modellvergleich (z.B. AR(2)-diff1: 0,29 vs. diff1: 0,18) → *KW §B.1*
- **Signifikanzrate** im Modellvergleich → *KW §B.3*
- **Erste Differenzen ΔY** als Hauptmodell-Transformation → *KW §C.2*
- **Saisonale Differenzen Δ₄Y** als alternative Transformation → *KW §C.3*

**Tests.**
- **t-Test auf φ₁** in jedem der vier Modelle → *T §1*

---

### 4.5.2 Stichprobenrobustheit

**Tabellen / Abbildungen.** Tab. 4.6 (φ₁-Mediane bei 100Q / 80Q / 60Q / 40Q); Abb. 4.4 (Stichprobenrobustheits-Plot).

**Werte.**
- **φ₁-Median** über vier Stichprobengrößen → *KW §A.1, §D.2*
- **Max. Δ (%)** — relative Abweichung vom 100Q-Wert → eigene Spalte zur Quantifizierung
- **Stichprobengröße n** pro Variante (931 / 1.230 / 1.854 / 2.355)

**Tests.** Keine eigenen — Vergleich rein deskriptiv über relative Differenzen.

---

### 4.5.3 Empirische Trennbarkeit der Quadrantendimensionen

**Tabellen / Abbildungen.** Tab. 4.7 (Spearman φ₁ × σ pro Kennzahl); Tab. 4.8 (χ²-Test auf Gleichverteilung der vier Quadranten); Abb. 4.9 (Streudiagramme im φ₁-σ-Raum).

**Werte.**
- **Spearman ρ** zwischen φ₁ und σ(ΔY) pro Kennzahl → *KW §E.1*
- **p-Wert (Spearman)** → *KW §B.2*
- **Quadranten-Häufigkeit** (beobachtet vs. erwartet n/4) — pro Kennzahl × Quadrant
- **χ²-Statistik** mit 3 Freiheitsgraden → *KW §E.2*
- **p-Wert (χ²)** → *KW §B.2*
- **Median-Splits** als Konstruktionsbasis der Quadranten → *KW §D.2*

**Tests.**
- **Spearman-Rangkorrelation** — primärer Trennbarkeits-Test → *T §2*
- **χ²-Test auf Gleichverteilung** — sekundäre Bestätigung über Quadranten-Häufigkeiten → *T §3*

---

### 4.5.4 Halbperioden-Vergleich (Pre-/Post-Finanzkrise) *— geplant, noch nicht ausgeführt*

**Tabellen / Abbildungen (geplant).** Tabelle Halbperioden-Vergleich; Boxplot φ₁ × Halbperiode (Side-by-Side, 7 Kennzahlen × 2 Perioden).

**Werte (geplant).**
- **φ₁_pre** für 2000 Q1 – 2012 Q4 → *KW §A.1*
- **φ₁_post** für 2013 Q1 – 2024 Q4 → *KW §A.1*
- **Differenz d_i = φ₁_post − φ₁_pre** pro Firma → ordinale Größe für Wilcoxon
- **σ_pre / σ_post** analog (optional)

**Tests (geplant).**
- **Wilcoxon-Vorzeichen-Rang-Test** — gepaarte Stichprobe (dieselbe Firma in beiden Perioden) → *T §6*

---

### 4.5.5 Asymmetrie der Mean-Reversion *— geplant, noch nicht ausgeführt*

**Tabellen / Abbildungen (geplant).** Tabelle Asymmetrie-Test; Forest-Plot φ₁⁺ vs. φ₁⁻ pro Kennzahl.

**Werte (geplant).**
- **φ₁⁺** — AR-Koeffizient nach positivem Vorquartalsschock → *KW §A.1*
- **φ₁⁻** — AR-Koeffizient nach negativem Vorquartalsschock → *KW §A.1*
- **Konfidenzintervalle / Standardfehler** der beiden Schätzer
- **Differenz φ₁⁺ − φ₁⁻** und zugehöriger p-Wert → *KW §B.2*
- **Residuum ε(t−1)** als Klassifikations-Variable → *KW §A.4*

**Tests (geplant).**
- **TAR(1) / Vorzeichen-Split** — primärer Asymmetrie-Test → *T §7*
- **Bonferroni-Korrektur** über die 7 Kennzahlen-Tests (α = 0,05 / 7 ≈ 0,007) → *T §8*

---

## Kompakt-Übersicht in einer Tabelle

| Abschnitt | Werte (neu eingeführt oder dominant) | Tests |
|---|---|---|
| **4 (Einl.)** | φ₁, σ(ΔY) | — |
| **4.1.1** | φ₁ Ø/Md/σ; σ(ΔY) Ø/Md/σ; Sig.%; t½ Q/J; R² | t-Test auf φ₁ |
| **4.1.2** | + IQR, p5/p95, ρ_σ ROE↔D/E (Vorgriff) | t-Test auf φ₁ |
| **4.1.3** | wie 4.1.2 | t-Test auf φ₁ |
| **4.1.4** | wie 4.1.2; + Levels-φ₁-Vorgriff | t-Test auf φ₁ |
| **4.2.1** | φ₁/σ/Sig.% pro Sektor × Kennzahl | — |
| **4.2.2** | Quadranten-Anteile (%); dominanter Quadrant | — |
| **4.3.1** | φ₁, t½, Levels-φ₁ (re-genutzt) | — |
| **4.3.2** | φ₁/σ pro Sektor (re-genutzt) | — |
| **4.3.3** | φ₁/σ/R²/p-Wert Einzelfirma; Consistency-Score | t-Test auf φ₁ |
| **4.4** | re-genutzt; Bonferroni-Vorschau | (Bonferroni-Vorschau) |
| **4.5.1** | φ₁ in 4 Modellen; φ₂; R²; Sig.%; ΔY, Δ₄Y | t-Test auf φ₁ pro Modell |
| **4.5.2** | φ₁-Median × 4 Stichproben; Max. Δ % | — |
| **4.5.3** | Spearman ρ; χ²; Quadranten-Häufigkeit | **Spearman**, **χ²** |
| **4.5.4** *(geplant)* | φ₁_pre, φ₁_post, Differenz | **Wilcoxon** |
| **4.5.5** *(geplant)* | φ₁⁺, φ₁⁻, Differenz, KI | **TAR(1)**, **Bonferroni** |

---

## Beobachtungen aus der Verortung

Drei Punkte fallen in der Gesamtsicht auf:

**(1) Wert-Inflation in 4.1.1.** Der Überblick führt sechs Wertkategorien ein (φ₁, σ, Sig.%, t½, R², plus Verteilungs-Statistiken). Das ist viel für einen Eingangsabschnitt — wenn Du den Einstieg straffen willst, kannst Du R² und σ-Verteilungs-Details in 4.1.2 und 4.1.3 schieben und in 4.1.1 nur φ₁-Hierarchie + Sig. + t½ behandeln. Aktuell ist es vollständig, aber dicht.

**(2) Tests sind zu 4.5.3 konzentriert.** Mit Ausnahme des t-Tests auf φ₁ (der eher implizit als Sig.-Rate auftaucht) findest Du explizite Tests nur in 4.5.3 (Spearman, χ²) und in den geplanten 4.5.4 (Wilcoxon) und 4.5.5 (TAR/Bonferroni). 4.1–4.4 ist deskriptiv-aggregierend. Das ist methodisch sauber: Du beschreibst zuerst, testest dann gezielt.

**(3) Re-Use-Stellen.** Die Werte aus 4.1 und 4.2 werden in 4.3 (Interpretation) und 4.4 (Erkenntnisse) weiterverwendet. Wenn Du in der Verteidigung einen Wert aus 4.3 erklärst, ist die Quelle immer ein Abschnitt aus 4.1/4.2 — die Verortungstabelle hilft, schnell die Referenz zu finden.
