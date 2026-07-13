# FF1 — Übersicht, Inventar & finalisierte Gliederung
> Arbeitsdatei. Stand: 21. April 2026. Ziel: Eine Datei, die den Stand von FF1 komplett abbildet — Daten, Grafiken, Textaussagen, Lücken, Gliederung.

---

## 0. Was ist wo? (Navigations-Map)

| Artefakt | Ort | Zweck |
|---|---|---|
| Aktueller Rohtext Kap. 5 | `Finale_Kapitel/Kapitel_5_FF1_Ergebnisse.md` | 170 Zeilen, AI-Rohfassung laut Autor — muss verfeinert werden |
| Publikations-Abbildungen | `Finale_Kapitel/Kapitel_5_Grafiken/abb_5_1..6.png` | 6 fertige Abbildungen mit konsistentem Design (DPI 200, deutsche Labels, Kategorie-Farbschema) |
| Grafik-Design-Brief | `Finale_Kapitel/Kapitel_5_Grafiken/README_GRAFIKEN.md` | Farben, Größen, Interpretationen — **Template für neue Abbildungen** |
| Roh-Plots (Notebook-Exporte) | `output/plots/ff1_*.png` | 12 FF1-Plots, keine Publikationsqualität, dienen als Vorlage/Entwurf |
| Primär-Zahlen (Text+Tabellen) | `output/ar/ar_summary_by_ratio.csv` | Alle 7 Kennzahlen mit φ₁-Median, σ, R², Signifikanzrate |
| Einzelschätzungen | `output/ar/ar_features_all.csv` | 26.084 Zeilen: 4 Modelle × ~932 Firmen × 7 Kennzahlen |
| Modellvarianten | `output/ar/ar_summary_by_model_ratio.csv` | diff1 / levels / AR(2) / diff4 → Tabelle 5.2 |
| Dimensions-Trennbarkeit | `output/ar/phi1_sigma_correlation.csv` | Spearman ρ(φ₁, σ) pro Kennzahl → Abschnitt 5.3.3 |
| Stichproben-Robustheit | `output/robustness/sample_comparison.csv` | 40Q / 60Q / 80Q / 100Q → Tabelle 5.3 |
| Finanzsektor | `output/robustness/financial_services.csv` | Vergleich Hauptanalyse vs. FinServ → Kap. 7.5, aber FF1-relevant |
| Notebook-FF1-Zellen | `analysis.ipynb` §§ 01.1–01.9 | Interaktive Plot-Familie mit Sektor-Filter |

---

## 1. Grafik-Inventar

### 1.1 In Kap. 5 bereits eingebunden (6 Stück, alle Publikations-Qualität)

| # | Datei (`Kapitel_5_Grafiken/`) | Verwendet in | Status |
|---|---|---|---|
| 1 | `abb_5_1_drei_schichten_boxplots.png` | 5.1 Hauptergebnis | ✅ fertig |
| 2 | `abb_5_2_signifikanz_r2.png` | 5.1 Drei Schichten | ✅ fertig |
| 3 | `abb_5_3_modellvergleich_tabelle.png` | 5.3.1 Modellvarianten | ✅ fertig |
| 4 | `abb_5_4_stichproben_robustheit.png` | 5.3.2 Stichprobenrobustheit | ✅ fertig |
| 5 | `abb_5_5_sektor_heatmap.png` | 5.4 Sektorale Heterogenität | ✅ fertig |
| 6 | `abb_5_6_sektor_quadranten.png` | 5.4 Drei Sektorgruppen | ✅ fertig |

Alle 6 sind hash-verschieden von den Rohfassungen in `output/plots/` — wurden also bewusst für die Publikation neu gebaut.

### 1.2 Frei verfügbar in `output/plots/` (14 Plots, nicht in Kap. 5 verwendet)

| Datei | Notebook-Zelle | Potenzieller Einsatz in Kap. 5 | Qualität |
|---|---|---|---|
| `ff1_phi1_boxplots.png` | 01.1 | = abb_5_1 (Rohfassung) | redundant |
| `ff1_sigma_boxplots.png` | 01.2 | **σ-Boxplot fehlt als Abb. — 5.1 neue Abbildung** | Entwurf, muss auf Template |
| `ff1_quadrant_scatter.png` | 01.3 | **φ₁×σ-Scatter alle 7 Kennzahlen — 5.3.3 neue Abbildung** | Entwurf |
| `ff1_roa_quadrant_methodik.png` | — | **ROA-Scatter für 5.3.3 / Kap. 4.1** (Zweite Medianlinie fehlt!) | Entwurf, Fix nötig |
| `methodik_phi1_vs_sigma.png` | — | Kap. 4 Quadrantenmethodik | Entwurf |
| `methodik_phi1_vs_sigma_v2.png` | — | Kap. 4 (neuere Version) | Entwurf |
| `ff1_quadrant_sector_bars.png` | 01.4 | ≈ abb_5_6 (alternative Darstellung) | redundant |
| `ff1_heatmap_phi1_sector.png` | — | = abb_5_5 (einzelne Kennzahl-Heatmap) | redundant |
| `ff1_heatmap_sigma_sector.png` | — | **σ-Heatmap pro Sektor — 5.4 als Zusatz** | Entwurf |
| `ff1_heatmap_signif_sector.png` | — | Signifikanz-Heatmap pro Sektor | optional |
| `ff1_signif_r2.png` | — | = abb_5_2 (Rohfassung) | redundant |
| `ff1_meanrev_comparison.png` | 01.5 | **Literatur-Benchmark-Vergleich — 5.1 neue Abbildung** | Entwurf |
| `ff1_meanrev_examples.png` | — | Einzel-Tickerzeitreihen als Illustration | didaktisch |
| `ff1_lag1_scatter.png` | — | φ₁-Scatter ΔY_t vs. ΔY_{t-1} | Methodik-Illustration |

**Fazit:** 4 klare Kandidaten für zusätzliche Abbildungen in Kap. 5 — alle müssen auf das Publikations-Template gehoben werden:
1. **σ-Verteilung Boxplots** (analog abb_5_1 für σ) — stützt Text in 5.1, 5.2.2, 5.2.3
2. **φ₁ × σ Scatterplot** (alle 7 Kennzahlen, Medianlinien) — für 5.3.3 empirische Trennbarkeit
3. **Literatur-Benchmark-Balkenplot** — φ₁ eigene Arbeit vs. Dichev & Tang (2009) — für 5.1.3 Theorie-Anbindung
4. **σ-Heatmap pro Sektor** — Komplement zu abb_5_5 — für 5.4

### 1.3 Notebook-FF1-Zellen (01.1–01.9)

| Zelle | Inhalt | Statischer Export | Empfehlung |
|---|---|---|---|
| 01.1 | φ₁-Boxplots mit Sektor-Filter | abb_5_1 | ✓ im Kap. |
| 01.2 | σ-Boxplots mit Sektor-Filter | `ff1_sigma_boxplots.png` | **→ abb_5_1b bauen** |
| 01.3 | Quadranten-Scatter (φ₁×σ) | `ff1_quadrant_scatter.png` | **→ abb_5_7 bauen** |
| 01.4 | Quadrantenverteilung pro Kennzahl | `ff1_quadrant_sector_bars.png` | für 5.1 optional |
| 01.5 | Benchmark φ₁ vs. Literatur | `ff1_meanrev_comparison.png` | **→ abb_5_2b bauen** |
| 01.6 | K-Means (Silhouette, ARI) | — | für Kap. 7 |
| 01.7 | FF1-Synthese-Tabelle | — | als Textblock in 5.5 |
| 01.8 | Modellvergleich-Panels | abb_5_3 | ✓ im Kap. |
| 01.9 | Stichproben + FinServ | abb_5_4 | ✓ Stichproben. FinServ = Kap. 7 |

---

## 2. CSV-Datenquellen pro Kapitelabschnitt

| Kap. 5 Abschnitt | CSV | Wird verwendet für |
|---|---|---|
| 5.1 Hauptergebnis + Tabelle | `ar_summary_by_ratio.csv` | φ₁-Mediane, σ, Signifikanz, R² aller 7 Kennzahlen |
| 5.2.1 ROA-Detailtabelle (Tab. 5.1) | `ar_features_all.csv` (Filter: model='diff1', ratio='ROA') | IQR, 5./95. Pz., Std, Signifikanz |
| 5.2.2–5.2.6 Einzelkennzahlen | `ar_features_all.csv` (Filter pro ratio) | Verteilungsparameter, sektorale Spannweiten |
| 5.3.1 Modellvarianten (Tab. 5.2) | `ar_summary_by_model_ratio.csv` | φ₁-Median für diff1, levels, AR(2), diff4 |
| 5.3.2 Stichproben (Tab. 5.3) | `sample_comparison.csv` | φ₁-Median für 100Q/80Q/60Q/40Q |
| 5.3.3 Trennbarkeit | `phi1_sigma_correlation.csv` | ρ_Spearman(φ₁, σ) pro Kennzahl |
| 5.4 Sektor-Analyse | `ar_features_all.csv` + profile-CSV | Sektor-Mediane pro Kennzahl |
| 5.5 Zusammenfassung | ar_summary_by_ratio.csv | finale Zahlen |

**Verifiziert:** alle CSVs existieren, Spaltennamen konsistent, Zahlen aus Rohtext matchen (ROA-φ₁-Median = −0,4315 im CSV ↔ −0,43 im Text ✓).

---

## 3. Gap-Analyse

### 3.1 Textaussagen in Kap. 5 ohne stützende Abbildung

| Textstelle | Aussage | Fehlende Abbildung |
|---|---|---|
| 5.1, 5.2.2, 5.2.3 | σ-Unterschiede zwischen Kennzahlen (ROA 0,017 vs. FCF 0,165 = Faktor 10) | σ-Boxplot-Abbildung fehlt |
| 5.1.3 | "Dichev & Tang (2009) dokumentieren vergleichbare AR(1)-Koeffizienten" | Benchmark-Balkenplot fehlt — wichtigster Theorie-Anker |
| 5.3.3 | "Die beiden Dimensionen erfassen weitgehend unterschiedliche Informationen" | φ₁×σ Scatterplot fehlt — Verweis geht nur auf Abb. 4.1 (ROA einzeln), aber Aussage gilt für alle 7 Kennzahlen |
| 5.4 Gruppe A | σ-Unterschiede zwischen Sektoren erwähnt | σ-Sektor-Heatmap fehlt — nur φ₁-Heatmap (abb_5_5) da |
| 5.2.4 FCF | "ρ(φ₁) = 0,15 zu buchhalterischen Kennzahlen" | Verweis auf FF2 ist OK; Kreuzverweis ausreichend |

### 3.2 Erweiterungspotenziale E5.1–E5.5 (Stand 4.4.2026)

| ID | Vorschlag | Status jetzt | Priorität |
|---|---|---|---|
| E5.1 | Halbperioden-Vergleich 2000–2012 vs. 2013–2024 | ⛔ noch nicht umgesetzt | Hoch, aber Aufwand mittel |
| E5.2 | Branchenspezifische AR-Dynamik interpretativ | 🔶 teilweise in 5.4 Sektorgruppen | Hoch, kann vertieft werden |
| E5.3 | Asymmetrie-Test (Plus-/Minus-Schocks) | ⛔ noch nicht umgesetzt | Hoch |
| E5.4 | Halbwertszeit t½ berechnen | 🔶 `hl_median` ist im CSV (0,33 Q für ROA ≈ 1 Monat!) aber nicht visualisiert | Gering, schneller Win |
| E5.5 | R²-Analyse (wo versagt AR(1)?) | 🔶 R² ist in Tab. 5.1 + abb_5_2, aber keine Residualanalyse | Mittel |

**Quick Wins vor Abgabe:**
- **E5.4 Halbwertszeit:** Ist schon als `hl_median` in der CSV (ROA: 0,33 Quartale ≈ 1 Monat). Ein kurzer Absatz in 5.1 plus Spalte in Tabelle der drei Schichten = **15 Minuten Arbeit**.
- **F5 (ERWEITERUNG): σ-Boxplots + Benchmark-Abb.** als abb_5_1b / abb_5_2b bauen = **60–90 Minuten**.

### 3.3 Inhaltlich-Methodische Offenlisten (aus COWORK_KONTEXT.md)

| # | Punkt | Ort |
|---|---|---|
| O1 | Zweite Medianlinie fehlt in Abb. 4.1 (ROA-Scatterplot) | `ff1_roa_quadrant_methodik.png` — in `generate_plots_v2.py` anpassen |
| O2 | Kap. 6.2.4 "Cramér's V" entfernen (FF2-Methodik-Korrektur) | Kap. 6, nicht FF1 |
| O3 | Interne Frage in 4.2.3 entfernen ("Pesaran macht der Ökonomische sachen?") | Kap. 4 |
| O4 | Literatur fehlt: Sloan (1996), Fama & French (2000) | **F&F 2000 liegt in `Literatur/PDFs/` ✓ — Sloan fehlt weiterhin** |

---

## 4. Finalisierte FF1-Gliederung (Vorschlag)

Geringfügige Anpassung der bestehenden Gliederung — neue/gebaute Abbildungen **fett markiert**.

```
5 Ergebnisse FF1: Systematische Dynamikmuster
5.1 Die Drei-Schichten-Hierarchie im Überblick
    5.1.1 Datenbasis & Modellgüte
          → R²-Verteilung, Signifikanzraten (abb_5_2 bestehend)
    5.1.2 Die drei Schichten: φ₁ und σ
          → Tabelle: φ₁-Median, σ-Median, HALBWERTSZEIT t½, R², n sig.
          → abb_5_1 bestehend (φ₁-Boxplots)
          → ★ abb_5_1b NEU: σ-Boxplots (gleicher Stil wie 5_1)
    5.1.3 Verbindung zur Theorie & Literatur
          → ★ abb_5_2b NEU: Balkenplot Eigene φ₁ vs. Dichev & Tang (2009)
          → Fairfield & Yohn (2001) als zweiter Vergleichspunkt

5.2 Detailanalyse pro Kennzahl
    5.2.1 ROA als Leitkennzahl (Tab. 5.1 bestehend)
    5.2.2 ROE — Leverage-Verstärkung
    5.2.3 EBIT-Marge — Operative Margendynamik
    5.2.4 FCF-Marge — Stärkste Veränderungskorrektur
    5.2.5 Current Ratio — Die Übergangszone
    5.2.6 Kapitalstruktur — Kein AR-Signal auf Differenzen

5.3 Robustheit
    5.3.1 Modellvarianten (Tab. 5.2, abb_5_3 bestehend)
    5.3.2 Stichprobenrobustheit (Tab. 5.3, abb_5_4 bestehend)
    5.3.3 Empirische Trennbarkeit der Quadrantendimensionen
          → Tabelle: ρ_Spearman(φ₁, σ) pro Kennzahl (aus phi1_sigma_correlation.csv)
          → ★ abb_5_7 NEU: φ₁×σ-Scatterplot alle 7 Kennzahlen (Small Multiples)
          → ALT: "Abb. 4.1 ROA-Scatter" bleibt in Kap. 4 (Methodik), bekommt zweite Medianlinie → O1-Fix

5.4 Sektorale Heterogenität
    5.4.1 Überblick: Heatmaps
          → abb_5_5 bestehend (φ₁-Heatmap)
          → ★ abb_5_5b NEU: σ-Heatmap pro Sektor (komplementär)
    5.4.2 Drei Sektorgruppen (abb_5_6 bestehend)
    5.4.3 Geschäftsmodell-Interpretationen (E5.2 vertiefen)

5.5 Zusammenfassung & Überleitung
    → Synthese-Tabelle aus Notebook-Zelle 01.7 als Textblock
```

**Vier neue Abbildungen, alle auf dem `README_GRAFIKEN.md`-Template.**

---

## 5. Next Actions (priorisiert, mit Aufwand)

| Prio | Action | Aufwand | Blockiert durch |
|---|---|---|---|
| 🔴 P1 | Halbwertszeit t½ in 5.1.2-Tabelle aufnehmen (Textfix + 1 Spalte) | 15 min | — |
| 🔴 P1 | Kap. 5 Rohtext auf Basis obiger Gliederung refinen (Ausformulierung + Literatur einbinden) | mehrere Sessions | — |
| 🟡 P2 | abb_5_1b (σ-Boxplots) nach Publikations-Template bauen | 30 min | Template-Code von abb_5_1 |
| 🟡 P2 | abb_5_2b (Literatur-Benchmark) bauen | 45 min | Dichev & Tang 2009 Zahlen verifizieren |
| 🟡 P2 | abb_5_7 (φ₁×σ-Scatter alle Kennzahlen) bauen | 30 min | — |
| 🟡 P2 | abb_5_5b (σ-Sektor-Heatmap) bauen | 30 min | — |
| 🟢 P3 | Abb. 4.1 ROA-Scatter: zweite Medianlinie in `generate_plots_v2.py` einfügen | 20 min | O1 Fix |
| 🟢 P3 | E5.1 Halbperioden-Vergleich als Zusatzabschnitt 5.3.4 | 2–3 h | neuer Code in `ar_model.py` |
| 🟢 P3 | E5.3 Asymmetrie-Test | 2–3 h | neuer Code |
| 🟢 P3 | Sloan (1996) beschaffen | — | extern |

---

## 6. Offene Entscheidungen (brauchen User-Input)

1. **E5.1/E5.3 (Halbperioden, Asymmetrie):** Reinpacken oder als Verteidigungs-Reserve? Bei 30 Tagen bis Abgabe: eher für Verteidigung aufsparen, aber E5.1 wäre inhaltlich stark.
2. **Neue Abbildungen abb_5_1b / abb_5_2b / abb_5_5b / abb_5_7:** Sollen wir heute direkt eine davon bauen (σ-Boxplots als low-hanging-fruit)? Oder erstmal nur planen und in separater Session bauen?
3. **Textarbeit Kap. 5:** Beginnen wir mit 5.1.2 (wo die neue t½-Spalte rein soll), oder mit 5.3.3 (wo die empirische Trennbarkeit ausformuliert werden muss)?

---

*Ende FF1_UEBERSICHT.md — wird fortgeschrieben.*
