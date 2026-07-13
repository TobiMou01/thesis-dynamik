# Erweiterungspotenziale & Arbeitsplan — Masterarbeit Mourier

**Stand:** 4. April 2026 | **Abgabe:** 21. Mai 2026 | **Verbleibend:** ~47 Tage

---

## 0. Grundsätzlicher Spirit

Die Arbeit liest sich aktuell wie eine mechanische Pipeline: AR(1) auf 7 Kennzahlen → Ergebnisse berichten → mit Literatur vergleichen. Was fehlt, ist **wissenschaftliche Eigeninitiative** — zusätzliche Analysen, die zeigen, dass du mitdenkst, Muster hinterfragst und über das Pflichtprogramm hinausgehst. Der Prof hat klar gesagt: **Interpretation ist das Hauptbewertungskriterium** (E15). Das heißt: Nicht nur "φ₁ ist -0,43 für ROA", sondern *warum*, *was bedeutet das wirtschaftlich*, und *was passiert, wenn ich das aus einem anderen Blickwinkel betrachte*.

**Leitprinzip für jede Erweiterung:** Nur einbauen, wenn sie eine **neue Interpretations-Ebene** eröffnet. Keine Analyse um der Analyse willen.

---

## 1. Kritische Fixes (SOFORT)

Diese Fehler existieren im aktuellen Dokument und müssen unabhängig von allen Erweiterungen behoben werden:

| # | Problem | Ort | Aufwand |
|---|---------|-----|---------|
| F1 | ~197 kaputte Umlaute (ae/oe/ue statt ä/ö/ü) | Kapitel 8 | 10 min (Suchen & Ersetzen) |
| F2 | Datenquelle "Compustat-Quarterly" → muss "EODHD Financial API" sein | Kap 1.3 | 2 min |
| F3 | TODO-Marker steht noch im Text: `[TODO: Feedback Prof. Steglich zu USGAAP vs. IFRS einarbeiten]` | Kap 4.1, ca. Paragraph 161 | 5 min |
| F4 | Befund 4 doppelt vorhanden | Kap 6, Paragraphen 342-343 | 2 min |
| F5 | Cramér's V in FF2 (Kap 6.2) zu prominent — Stollhoff: nur für FF3 erlaubt (E11) | Kap 6.2 | 15 min (kürzen/umstrukturieren) |

---

## 2. Erweiterungen nach Kapitel

### Kapitel 5 — FF1: Systematische Dynamik

| ID | Vorschlag | Was es bringt | Aufwand | Priorität |
|----|-----------|---------------|---------|-----------|
| E5.1 | **Halbperioden-Vergleich** (2000-2012 vs. 2013-2024): AR(1) separat schätzen, φ₁ vergleichen | Zeigt ob Mean-Reversion sich über die Zeit verändert hat (Post-Finanzkrise-Regime?) | Mittel (Code anpassen in `ar_model.py`) | ⭐⭐⭐ HOCH |
| E5.2 | **Branchenspezifische AR-Dynamik**: φ₁-Verteilungen nach GICS-Sektor aufschlüsseln, nicht nur als Heatmap, sondern interpretativ: *Warum* ist φ₁ bei Utilities anders als bei Tech? | Wirtschaftliche Erklärung statt nur Deskription | Gering (Daten da, nur Interpretation) | ⭐⭐⭐ HOCH |
| E5.3 | **Asymmetrie-Test**: Ist Mean-Reversion nach positiven Schocks genauso stark wie nach negativen? (Split der Residuen nach Vorzeichen) | Zeigt ob z.B. Gewinnerholung asymmetrisch ist — ökonomisch extrem spannend | Mittel | ⭐⭐⭐ HOCH |
| E5.4 | **Halblebensdauer** (t½ = ln(0.5)/ln(1+φ₁)): Für jede Kennzahl berechnen und in Jahren interpretieren | Macht φ₁ greifbar: "ROA-Schocks sind nach ~1.2 Jahren halb abgebaut" | Gering (reine Rechnung) | ⭐⭐ MITTEL |
| E5.5 | **R²-Analyse**: Wie viel Varianz erklärt das AR(1)-Modell? Wo versagt es systematisch? | Ehrliche Selbstreflexion → zeigt wissenschaftliche Reife | Gering (R² schon da) | ⭐⭐ MITTEL |

### Kapitel 6 — FF2: Interdependenzen & Events

| ID | Vorschlag | Was es bringt | Aufwand | Priorität |
|----|-----------|---------------|---------|-----------|
| E6.1 | **Cross-Ratio Lead-Lag-Analyse**: Geht ein Profitabilitätsschock einem Liquiditätsschock voraus? (Kreuzkorrelation mit Lags) | Zeigt kausale Ketten zwischen den Schichten — das ist echter Mehrwert | Hoch (neuer Code) | ⭐⭐⭐ HOCH |
| E6.2 | **Event-Heterogenität**: Nicht nur "COVID-Effekt auf Volatilität", sondern: Welche Branchen reagieren anders? (Interaktion Event × Sektor) | Differenziertere Event-Analyse statt Einheitsbrei | Mittel | ⭐⭐⭐ HOCH |
| E6.3 | **Schicht-Kopplungs-Index**: Eigene Metrik entwickeln, die misst wie stark Profitabilität-Liquidität-Kapitalstruktur gekoppelt sind | Eigenständiger methodischer Beitrag — hebt die Arbeit deutlich | Hoch | ⭐⭐ MITTEL |
| E6.4 | **Korrelations-Stabilität über Zeit**: Korrelationsmatrix in 5-Jahres-Fenstern → Hat sich die Kopplung verändert? | Zeigt temporale Dynamik der Interdependenz | Mittel | ⭐⭐ MITTEL |
| E6.5 | **Bonferroni konsequent umsetzen**: 42 Tests bei Korrelationsmatrizen → α_korr = 0,05/42 = 0,00119 | Pflicht laut Stollhoff E14 | Gering | ⭐⭐⭐ PFLICHT |

### Kapitel 7 — FF3: Externe Validierung

| ID | Vorschlag | Was es bringt | Aufwand | Priorität |
|----|-----------|---------------|---------|-----------|
| E7.1 | **Größeneffekte vertiefen**: Nicht nur Spearman-Korrelation, sondern Quintil-Analyse (φ₁ nach Größenquintilen) mit wirtschaftlicher Interpretation | Zeigt ob kleine Firmen wirklich volatiler sind und warum | Mittel | ⭐⭐⭐ HOCH |
| E7.2 | **Temporale Konsistenz**: Wie stabil ist die Quadrant-Zuordnung über Zeit? (Übergangsmatrix zwischen Halbperioden) | Prüft ob Dynamik-Profile Firmen-inhärent sind oder sich verändern | Mittel | ⭐⭐⭐ HOCH |
| E7.3 | **Fallstudien**: 3-5 Firmen im Detail analysieren (z.B. Apple, Tesla, eine Bank, ein Versorger) — φ₁-Werte mit realer Firmengeschichte verbinden | Macht Statistik greifbar, zeigt Storytelling-Kompetenz | Gering (Daten da) | ⭐⭐⭐ HOCH |
| E7.4 | **Finanzsektor-Deep-Dive**: Nicht nur "Finanzsektor ausgeschlossen weil anders", sondern: *Wie* genau anders? Eigener Robustness-Abschnitt | Zeigt, dass Ausschluss begründet ist, nicht willkürlich | Gering (Daten in `robustness/`) | ⭐⭐ MITTEL |
| E7.5 | **Bonferroni für χ²-Tests**: 7 Tests → α_korr = 0,05/7 = 0,00714 | Pflicht laut Stollhoff E14 | Gering | ⭐⭐⭐ PFLICHT |

### Kapitel 8 — Diskussion & Limitationen

| ID | Vorschlag | Was es bringt | Aufwand | Priorität |
|----|-----------|---------------|---------|-----------|
| E8.1 | **Ehrliche Modellkritik**: Wo versagt AR(1)? GARCH-Vergleich als Benchmark (nicht als Hauptmodell, nur zur Einordnung) | Zeigt Reflexionsfähigkeit | Mittel | ⭐⭐ MITTEL |
| E8.2 | **"Was wäre wenn"-Abschnitt**: Wie hätten sich Ergebnisse mit IFRS-Daten oder europäischen Firmen verändert? Hypothesen formulieren | Zeigt Weitblick über die eigene Arbeit hinaus | Gering (nur Text) | ⭐⭐ MITTEL |
| E8.3 | **Implikationen für Praxis**: Was bedeuten die Ergebnisse für Analysten, Portfoliomanager, Kreditrisiko? | Macht die Arbeit relevant über Akademia hinaus | Gering (nur Text) | ⭐⭐⭐ HOCH |

---

## 3. Code-Architektur — Was passiert wo?

### Source-Dateien (`src/`)

| Datei | Zeilen | Funktion | Erzeugt (Output) |
|-------|--------|----------|-------------------|
| `config.py` | 380 | Zentrale Konfiguration: Pfade, Zeitraum, Kennzahlen-Definition, Schwellenwerte, Farben | — |
| `load_data.py` | 613 | Daten laden (EODHD API-Cache), Filterkette (5871→932 Firmen), Outlier-Detection, Winsorizing | `output/ratios/ratio_panel.csv`, `output/preprocessing/` |
| `ar_model.py` | 276 | AR(1)-Schätzung auf erste Differenzen ΔY, p-Werte, R², Signifikanztests | `output/ar/ar_features.csv`, `ar_features_all.csv`, `ar_summary_by_ratio.csv`, `ar_summary_by_model_ratio.csv`, `phi1_sigma_correlation.csv` |
| `classify.py` | 334 | Quadrant-Klassifikation (Median-Split φ₁ × σ), K-Means Clustering (2 Varianten) | `output/clustering/quadrant_*.csv`, `kmeans_*.csv` |
| `company_profiles.py` | 483 | Firmenprofile, Konsistenz-Scores, dominante Quadranten | `output/profiles/company_quadrant_profiles.csv`, `consistency_summary.csv` |
| `external_validation.py` | 173 | FF3: χ²-Tests, Cramér's V, Größeneffekte (Spearman) | `output/profiles/ff3_chi2_results.csv`, `ff3_size_effects.csv` |
| `robustness_samples.py` | 423 | Variable Sample-Größen (40Q-100Q), Finanzsektor-Vergleich | `output/robustness/sample_comparison.csv`, `financial_services.csv` |
| `export_ff1_charts.py` | 263 | Alle FF1-Grafiken (Boxplots, Heatmaps, Scatter, Quadrant-Visualisierungen) | `output/plots/ff1_*.png` |
| `export_raw_panel.py` | 129 | Rohdaten-Export für externe Nutzung | `output/ratios/ratio_panel.csv` |

### Haupt-Notebook

| Datei | Zellen | Funktion |
|-------|--------|----------|
| `analysis.ipynb` | 112 | Orchestriert die gesamte Pipeline: lädt Module, ruft Funktionen, erzeugt Plots, exportiert CSVs |

### Output-Verzeichnisse

| Verzeichnis | Inhalt | Relevant für |
|-------------|--------|--------------|
| `output/ar/` | AR(1)-Schätzungen, Zusammenfassungen, φ₁-σ-Korrelation | FF1 (Kap 5) |
| `output/clustering/` | Quadrant-Zuordnungen, K-Means-Ergebnisse | FF1 (Kap 5) |
| `output/interdependence/` | Korrelationsmatrizen (φ₁, σ), p-Werte, Quadrant-Kreuztabellen | FF2 (Kap 6) |
| `output/profiles/` | Firmenprofile, Konsistenz, χ²-Tests, Größeneffekte | FF3 (Kap 7) |
| `output/robustness/` | Sample-Vergleiche, Finanzsektor-Analyse | Kap 7/8 |
| `output/explore/` | Peak-Windows, Volatilitäts-Scores, Event-Fenster | FF2 (Kap 6) |
| `output/ratios/` | Basis-Ratiopanel (932 × 100Q × 7 Kennzahlen) | Alle Kapitel |
| `output/plots/` | 31+ PNG-Grafiken (ff1_*, ff2_*, ff3_*, methodik_*) | Alle Kapitel |

### Die 7 Kennzahlen und ihre Schichten

| Schicht | Kennzahl | φ₁ (Median) | Interpretation |
|---------|----------|-------------|----------------|
| **Profitabilität** | ROA, ROE, Profit Margin | ≈ −0,43 | Starke Mean-Reversion |
| **Liquidität** | Current Ratio, Quick Ratio | ≈ −0,17 | Moderate Mean-Reversion |
| **Kapitalstruktur** | Debt/Equity, Debt/Assets | ≈ −0,04 | Schwache Mean-Reversion (nahezu Random Walk) |

---

## 4. Wo im Code müssen Erweiterungen eingebaut werden?

| Erweiterung | Primäre Datei | Neue Datei nötig? | Output-Ziel |
|-------------|---------------|-------------------|-------------|
| E5.1 Halbperioden | `ar_model.py` | Nein, Parameter ergänzen | `output/ar/ar_subperiod_comparison.csv` |
| E5.3 Asymmetrie | `ar_model.py` | Evtl. `src/asymmetry.py` | `output/ar/asymmetry_test.csv` |
| E5.4 Halblebensdauer | `ar_model.py` oder Notebook | Nein | Tabelle in Arbeit |
| E6.1 Lead-Lag | Neuer Code | `src/lead_lag.py` | `output/interdependence/cross_correlations.csv` |
| E6.2 Event×Sektor | `explore/` Logik + Notebook | Nein | `output/explore/event_sector_interactions.csv` |
| E6.4 Korr-Stabilität | Notebook oder `src/interdependence.py` | Optional | `output/interdependence/corr_windows.csv` |
| E7.1 Größen-Quintile | `external_validation.py` | Nein, erweitern | `output/profiles/size_quintile_analysis.csv` |
| E7.2 Übergangsmatrix | `company_profiles.py` | Nein, erweitern | `output/profiles/transition_matrix.csv` |
| E7.3 Fallstudien | Notebook | Nein | Narrative in Arbeit |

---

## 5. Zeitplan: 4. April → 21. Mai 2026

### Übersicht

| Phase | Zeitraum | Tage | Fokus |
|-------|----------|------|-------|
| **Phase 1: Code & Analysen** | 4.-18. April | 15 | Code aufräumen, Erweiterungen implementieren, neue CSVs/Plots |
| **Phase 2: Schreiben** | 19. April - 8. Mai | 20 | Kapitel überarbeiten, neue Ergebnisse einbauen, Interpretation vertiefen |
| **Phase 3: Feinschliff** | 9.-17. Mai | 9 | Korrekturlesen, Formatierung, Quellencheck, Umlaute fixen |
| **Phase 4: Puffer** | 18.-21. Mai | 4 | Finale Durchsicht, Druck/Abgabe |

### Detailplan Phase 1 (Code)

| Woche | Tage | Aufgaben |
|-------|------|----------|
| KW 15 (6.-10. Apr) | 5 | Code aufräumen, `config.py` bereinigen, kritische Fixes F1-F5, Bonferroni implementieren (E6.5, E7.5) |
| KW 16 (13.-17. Apr) | 5 | E5.1 Halbperioden, E5.3 Asymmetrie, E5.4 Halblebensdauer, E7.3 Fallstudien vorbereiten |
| Optional bis 18. Apr | – | E6.1 Lead-Lag (falls Zeit), E7.1 Größen-Quintile |

### Detailplan Phase 2 (Schreiben)

| Woche | Tage | Aufgaben |
|-------|------|----------|
| KW 17 (20.-24. Apr) | 5 | Kap 4 (Methodik) + Kap 5 (FF1) überarbeiten — neue Ergebnisse + Interpretation |
| KW 18 (27. Apr-1. Mai) | 5 | Kap 6 (FF2) + Kap 7 (FF3) überarbeiten — Erweiterungen einbauen |
| KW 19 (4.-8. Mai) | 5 | Kap 8 (Diskussion) vertiefen, Kap 9 (Fazit) schärfen, Kap 1-3 finalisieren |

### Detailplan Phase 3 (Feinschliff)

| Woche | Tage | Aufgaben |
|-------|------|----------|
| KW 20 (11.-15. Mai) | 5 | Vollständiger Durchgang: Umlaute, Verweise, Tabellen, Abbildungsverzeichnis, Literaturverzeichnis |
| 16.-17. Mai | 2 | Fremdes Auge lesen lassen, letzte Korrekturen |

### Risikopuffer

4 Tage (18.-21. Mai) sind bewusst freigehalten. Bei diesem Zeitplan hast du **realistisch genug Zeit**, um die wichtigsten Erweiterungen (E5.1, E5.2, E5.3, E5.4, E7.3 und die Pflicht-Bonferrroni-Korrekturen) einzubauen. Die aufwändigeren Erweiterungen (E6.1 Lead-Lag, E6.3 Kopplungs-Index) sind nice-to-have — nur machen wenn Phase 1 schneller geht als geplant.

---

## 6. Priorisierte Reihenfolge (Empfehlung)

**Muss (erste Woche):**
1. F1-F5: Kritische Fixes
2. E6.5 + E7.5: Bonferroni (Stollhoff-Pflicht)
3. E5.4: Halblebensdauer (10 min Arbeit, großer Interpretations-Gewinn)
4. E5.2: Branchenspezifische Interpretation vertiefen (kein neuer Code nötig)

**Sollte (zweite Woche):**
5. E5.1: Halbperioden-Vergleich
6. E5.3: Asymmetrie-Test
7. E7.3: Fallstudien (3-5 Firmen)
8. E7.1: Größen-Quintile
9. E8.3: Praxis-Implikationen

**Kann (wenn Zeit bleibt):**
10. E6.1: Lead-Lag-Analyse
11. E6.2: Event×Sektor-Interaktion
12. E7.2: Übergangsmatrix
13. E6.4: Korrelations-Stabilität
14. E6.3: Kopplungs-Index
15. E8.1: GARCH-Benchmark

---

## 7. Stollhoff-Entscheidungen (Referenz)

| Code | Entscheidung | Status |
|------|-------------|--------|
| E10 | Monte Carlo RAUS | ✅ Umgesetzt |
| E11 | Cramér's V: nur für FF3, nicht für FF2 | ⚠️ Kap 6.2 noch zu prominent |
| E12 | Keine neuen Kennzahlen | ✅ |
| E13 | Kein Europa-Vergleich | ✅ |
| E14 | Bonferroni-Korrektur | ⚠️ Noch nicht im Code/Text |
| E15 | Interpretation = Hauptbewertungskriterium | 🔴 Hier liegt der größte Hebel |
