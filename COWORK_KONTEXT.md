# COWORK_KONTEXT.md
> Lebende Projektdatei — wird nach jeder Session aktualisiert.
> Letzte Aktualisierung: 28. April 2026 (Session „v4-Master + Custom-Ratios + Schicht-Tabellen + 4.1-Vertiefung")

---

## 🆕 Stand 28.04.2026 — Was diese Session geliefert hat

### Master-Doc-Version
- **`Text/Kapitel_4_FF1_Ergebnisse_Entwurf_v4.docx` ist neuer Master.** V3 bleibt als Backup. Künftige Änderungen überschreiben v4 direkt (keine v5 angelegt). Stand v4: 13 Tabellen + 10 Bilder.
- Tobi hat Para zu Kap.-4-Einleitung und Para 010 (4.1-Big-Picture-Erklärung) selbst formuliert und im Doc gespeichert. Diese Texte sind jetzt verbindlich.

### Pipeline-Erweiterung — Custom-Ratios
- **`INCLUDE_CUSTOM_RATIOS = True`** in `src/config.py`
- **Quick Ratio neu** in `src/custom_ratios.py` (zusätzlich zu CCC, Net Debt/EBITDA, Bruttomarge auskommentiert)
- **Aktive Custom-Ratios:** Cash Conversion Cycle, Quick Ratio, Net Debt/EBITDA. Bruttomarge bleibt definiert aber nicht aktiv (DuPont liefert interne Robustheit für Profitabilität).
- **Pipeline gelaufen:** 9.313 AR-Schätzungen über 932 Ticker × 10 Kennzahlen (vorher 6.521 mit 7 Kennzahlen).
- **Bug gefixt:** `_filter_nan_tickers` in `src/load_data.py` filtert jetzt formula-basierte Ratios mit leerem `numerator_col`/`denominator_col` aus der NaN-Prüfung aus.

### FF1-Befunde aus Custom-Ratios
- **Quick Ratio ≈ Current Ratio** (φ₁ = −0,18 vs. −0,17, R² ≈ 0,03 beide). Bestätigt die Bestand-Mechanik.
- **CCC stark abweichend:** φ₁ = −0,37, R² = 0,14, 97 % φ<0. Stromgröße verhält sich fundamental anders als Bestand.
- **Net Debt/EBITDA verhält sich wie Profitabilität:** φ₁ = −0,46, R² = 0,21, 99 % φ<0, 62 % Bonferroni-signifikant. Cashflow-Bezug bricht die „Modell-erklärt-nichts"-Aussage von Buchwert-Kapitalstruktur auf.

### v4-Doc strukturelle Änderungen
- **Tab 1 (Master-Tabelle 4.1.1) entfernt** — der Inhalt wurde aufgeteilt auf die drei Schicht-Tabellen 4.1.2/4.1.3/4.1.4.
- **Schicht-Tabellen 4.1.2/4.1.3/4.1.4 transponiert:** Statistik-Kategorien als Zeilen, Kennzahlen als Spalten. Mit Cell-Splitting (Median + IQR pro Zelle gestapelt). 
- **Schicht-Tabellen erweitert um Custom-Ratios als Vergleichspunkte:**
  - 4.1.2 Profitabilität: ROA, ROE, EBIT-M, FCF-M (keine Custom — DuPont reicht)
  - 4.1.3 Liquidität: Current Ratio, Quick Ratio*, CCC*
  - 4.1.4 Kapitalstruktur: D/E, EK-Quote, Net Debt/EBITDA*
  - Sternchen markiert Vergleichspunkte
- **Halblebensdauer-Sprache komplett raus aus 4.1.** Hinweis-Absatz mit ln(0,5)-Formel entfernt. Halblebensdauer-Bezüge in 4.3.x und 4.4 stehen noch (zur Schreibarbeit-Phase).
- **Big-Picture Joint Plot** als Abb. 4.1 unter „## 4.1" eingefügt (Joint Plot φ₁ × σ, log-skaliert mit Dezimal-Beschriftung, drei Schichten farblich, Marginal-Boxplots, Quadranten-Linien).
- **KDE-Overlays** ersetzen die alten 7 Mini-KDE-Plots in 4.1.1 (eine Grafik für φ₁, eine für σ, alle 7 Kennzahlen überlagert mit Median in der Legende).
- **Mini-Scatter** (φ₁ × σ pro Kennzahl, Quadranten-gefärbt) auf 4.1.2/4.1.3/4.1.4 aufgeteilt — Profitabilität 4 Plots, Liquidität 1, Kapitalstruktur 2.

### v4-Doc inhaltliche Vertiefung in 4.1
Drei Paragraphen wurden auf Daten-Beobachtungs-Ebene vertieft (ohne Theorie/Interpretation):
- **Para 014 (4.1.1 Eröffnung):** φ₁-Werte konkret aufgeführt, alle 7 Mediane negativ → universelle Mean-Reversion-Tendenz auf Stichprobenebene. Bonferroni und Signifikanzraten herausgenommen, weil sie in den Schicht-Tabellen erscheinen.
- **Para 018 (zur φ-KDE):** 95. Perzentile pro Kennzahl, Sign-Anteile pro Kennzahl (36 % bei EK-Quote, 28 % bei D/E, 11 % bei Current Ratio, <2 % bei Profitabilität). Plus Brücken-Hinweis: „Sub-Wolken der Kapitalstruktur sind in φ-KDE nicht sichtbar, weil ihre Trennung primär auf der σ-Achse liegt".
- **Para 022 (zur σ-KDE):** σ-Spannweite Faktor 19 zwischen ROA und Current Ratio, σ-Reihenfolge weicht vom φ-Ranking ab (auf ROA folgt EK-Quote, nicht ROE), D/E ≈ FCF-Marge im σ-Niveau.

### Notebook-Status (kap4_FF1.ipynb)
- 61 Cells, 18 Plots, 0 Errors. Big-Picture als Cell direkt unter 4.1.1, dann KDE-Overlays, dann Schicht-Mini-Scatter.
- Achsen-Beschriftung Big-Picture: log-skaliert mit FuncFormatter-Dezimal (`{x:g}`) und `minorticks_off()`.

### Memory-System aktualisiert
- **Neue Datei:** `feedback_schreibstil.md` — präzise Subjekt-Verb-Beziehung, konsistente Terminologie (Dynamiktypen statt Plateaus/Schichten), keine Meta-Floskeln, Verben variieren, vor Doc-Ersetzung Inhalt zeigen.
- MEMORY.md Index aktualisiert.

### Offene Punkte aus FF1 (für nächste Session)
1. **Para 022 (σ-KDE-Beschreibung)** — könnte selbstkritisch nochmal durchgegangen werden, ist aktuell „bestätigt-Stakkato"-frei aber eventuell noch zu nüchtern.
2. **Halblebensdauer-Bezüge in 4.3.x und 4.4** entfernen (Tobi hatte angemerkt dass das insgesamt raus soll).
3. **Caption-Texte in 4.1.1** — alte Captions („Verteilung pro Kennzahl") passen nicht mehr ganz zu den Overlay-Plots, sollten beim Schreiben angepasst werden.
4. **Sign-Gruppen-Vertiefung in 4.1.4** — geplant: separate Sign-Tabelle (φ<0 vs. φ>0) für D/E und EK-Quote, Trajektorien-Plot (Median-Niveau Q1=100 normalisiert) — nach FF1-Schreibarbeit.
5. **4.5.5 Asymmetrie-Hinweis:** kurzer Texteinschub zur Trennung Sign-Gruppen (zwischen Firmen) vs. Sign-Dummy-AR (innerhalb Zeitreihe).
6. **Methodik (Kap. 3):** 6.521 vs. 6.524 noch zu korrigieren.

### Schreibarbeit-Strategie (von Tobi etabliert)
- Inhaltliche Tiefe statt methodischer Tiefe
- Datennahe Beobachtungen direkt am Plot/Daten verankern
- Inline-Interpretation (Befund + kurze Deutung in Klammern) statt eigene Interpretationskapitel
- Keine Bonferroni/Signifikanz-Aussagen in Sub-Kapiteln vor den Tabellen, in denen sie als Spalten erscheinen
- Bei Doc-Ersetzungen: aktuellen Para-Inhalt zeigen, Tobis OK abwarten, dann erst überschreiben

---

## 🆕 Stand 26.04.2026 — Was diese Session geliefert hat

### Code & Architektur
- **`src/config.py` + `src/load_data.py`**: erweitert um `RatioDef.formula`-Feld, neue Custom-Kennzahlen können per Formel definiert werden (Backups in `*.backup_2026-04-26`).
- **`src/custom_ratios.py` (neu)**: drei Beispiel-Definitionen (Gross Margin, Cash Conversion Cycle, Net Debt/EBITDA), aktivierbar über `INCLUDE_CUSTOM_RATIOS = True`.
- **`src/analysis_helpers.py` (neu)**: ~360 Zeilen Daten-Helper für die Notebook-Layer (13 Loader, 4 Aggregations-Funktionen, 5 Stats-Funktionen, ohne Plot-Code).
- **`src/kap4_extensions.py` (existiert)**: E5.4 Halblebensdauer + E6.5/E7.5 Bonferroni + 4 Kap.-4-spezifische Plot-Funktionen.
- **`notebooks/` (neu)**: 5 Notebook-Skelette für die Hauptkapitel. `kap4_FF1.ipynb` voll ausgebaut (54 Zellen, 12 Plots, 14 Tabellen, läuft fehlerfrei). Skelette für Kap. 1–3, 5, 6, 7 angelegt.

### Berechnungen (zusätzlich zu den FF1-Outputs)
- **E5.1 Halbperioden-Vergleich**: AR(1) separat für 2000Q1–2012Q4 vs. 2013Q1–2024Q4. Outputs `ar_subperiod_comparison.csv` + `ar_subperiod_summary.csv`. **Befund**: ROA und ROE post-2013 signifikant stärker mean-revertierend (−0,04, p < 0,001), andere Kennzahlen stabil.
- **E5.3 Asymmetrie-Test**: TAR(1) mit Vorzeichen-Split. Outputs `asymmetry_test.csv` + `asymmetry_summary.csv`. **Befund**: alle 7 Kennzahlen Bonferroni-resistent asymmetrisch. Profitabilität: φ⁻ deutlich stärker negativ als φ⁺ (Konservatismus-Hypothese). Bilanzstruktur: umgekehrtes Muster (Schulden-Momentum).

### Kap. 4 — drei Versionen liegen vor
| Version | Datei | Wörter | Charakteristik |
|---|---|---:|---|
| V1 | `Text/Kapitel_4_FF1_Ergebnisse_Entwurf.docx` | ~11.500 | Volle Ausführung, viele Wiederholungen, Vertiefungs-Marker offen |
| V2 | `Text/Kapitel_4_FF1_Ergebnisse_Entwurf_v2.docx` | 5.371 | Konsolidiert, σ-Block in 4.3.2, Vertiefungen ausgefüllt, 4.5.4 nach FF2 verschoben |
| V3 | `Text/Kapitel_4_FF1_Ergebnisse_Entwurf_v3.docx` | 4.776 | V2 im Mourier-Schreibstil (keine Gedankenstriche, keine Semikolons außer Zitationen, kompaktere Sätze) — **aktuelle Arbeitsfassung** |

V1 + V2 als historische Referenz, **V3 als Master**.

### Offene Punkte zu Kap. 4 (für nächste Session)
1. **σ-Achsen-Strategie**: Bei `ff1_sigma_kde.png` und `ff1_phi1_sigma_scatter.png` aktuell Variante B (gleiche Tick-Anzahl, individuelle Skala). Tobi noch unentschieden zwischen (a) Status quo, (b) echte gleiche x-Achse, (c) gruppiert nach Wertebereich. Default: Status quo.
2. **4.3.4 / 4.3.5 Trennung**: Beispielfirmen aus 4.3.4 in eigene Sektion 4.3.5 verschieben; in 4.3.4 die DuPont-Brücke über die σ-Boxplots aus 4.1.2 (Faktor 2,8 zwischen σ-ROE und σ-ROA) konkret ankern. Argumentlinie ist abgestimmt, Implementierung steht aus.
3. **Renumerierung**: Beispielfirmen-Grafik aktuell als Abb. 4.6 in 4.3.4. Bei 4.3.5-Verschiebung nochmal numerieren.
4. **Sigma-Boxplot-Bezug von 4.1.2 zu 4.3.4** als verzahnter Verweis ausformulieren — ist die DuPont-Brücke ohne Beispielfirmen-Mismatch.
5. **Methodik (Kap. 3)**: 6.521 vs. 6.524 — Methodik nennt 6.524 (theoretisch 932×7), tatsächlich 6.521 nach NaN-Filter. Bei Methodik-Edit anpassen.
6. **E5.1/E5.3-Befunde** sind in Kap. 4 V3 noch in 4.5.5 drin (Asymmetrie). 4.5.4 (Halbperioden) bewusst ausgelagert nach FF2. Daten und Tabellen liegen vor, müssen in FF2 eingebaut werden.

---

## 🎯 FF2-Architektur (Stand 26.04.2026)

Tobis Verständnis (richtig): FF2 hat drei Teilfragen:

1. **Querschnittliche Interdependenz, gleiche Zeit** — Spearman-Korrelationsmatrizen φ₁ × φ₁ und σ × σ. ✅ existiert in `output/interdependence/corr_*.csv` mit Bonferroni-Markierung (E6.5).
2. **Querschnittliche Interdependenz, verschobene Zeit** — Lead-Lag-Analyse mit Cross-Korrelation. ❌ E6.1, Spezifikation existiert (siehe `Text/E6.1_Spezifikation.md` falls vorhanden, sonst neu anzulegen), Code (`src/lead_lag.py`) und Outputs noch nicht.
3. **Zeitliche Events mit Branchen-Heterogenität** — Peak-Windows + Quadranten-Reaktionen + Sektor-Reaktionen. ✅ existiert (`peak_windows.csv`, `volatility_scores.csv`, `ff2_quadrant_reactions.png`).

**Ergänzungen zu Tobis Verständnis:**
- Bei „σ-Interdependenz" misst hohe Korrelation eine **Schwankungs-Kopplung**, nicht „beide haben Mean-Reversion". Beispiel: ROE × D/E (ρ_σ = 0,82) — DuPont-Hebel.
- Bei „Events: vor/während/nach φ und σ" ist die „vor/während/nach"-Differenzierung **noch nicht implementiert**, aktuell wird nur „während" ausgewertet. Wäre eine starke Erweiterung.

### Halbperioden-Stabilität (E5.1) gehört zu FF2
Aus FF1 verschoben (Kap. 5.x). Daten liegen vor (`ar_subperiod_summary.csv`). **Befund**: Profitabilitäts-Mean-Reversion in der Post-Krise-Periode signifikant stärker (Konvergenzbeschleunigung). Andere Kennzahlen stabil.

---

## 🔄 Nummerierungs-Shift 22./23.04.2026

Die Kapitelgliederung wurde kompakter gemacht — Einleitung/Theorie/Methodik zusammengezogen:

| Alte Nummer | Neue Nummer | Inhalt |
|---|---|---|
| Kap. 5 | **Kap. 4** | Ergebnisse FF1 |
| Kap. 6 | **Kap. 5** | Ergebnisse FF2 (Interdependenzen + Events) |
| Kap. 7 | **Kap. 6** | Ergebnisse FF3 (Externe Validierung) |
| Kap. 8 | **Kap. 7** | Diskussion |
| Kap. 9 | **Kap. 8** | Fazit |

Innerhalb jedes Ergebnis-Kapitels gilt jetzt die Makro-Struktur **Methodik/Ergebnisse → Interpretation → Erkenntnisse → Robustheit**. FF3 (Kap. 6) ist die einzige Ausnahme: Interpretation bleibt direkt bei den Ergebnis-H2 (keine separate Interpretation-H2).

Aktueller Scaffold gebaut über `build_arbeitstext.js` → `Text/Arbeitstext.docx`. Word-Inhalt wird bei jedem Rebuild überschrieben — **vor Rebuild Backup** (`Arbeitstext_backup_YYYY-MM-DD_HHMM.docx`).

## 🎨 Notiz-Helper im build_arbeitstext.js

- `notiz([{label, text}])` — graue/gelbliche Standard-Notiz für Platzhalter, Prof-Zitate, Meta-Hinweise
- `grafikFehlt({art, was, daten, zweck})` — **grün-kursiv**, 📊/ℹ️ Prefix. Für fehlende Grafiken (`art: "Grafik"`) oder fehlende Tabelleninfos (`art: "Info"`)
- `fallbeispiel({was})` — **orange-kursiv**, 🎯 Prefix. Für eingestreute Firmenbeispiele im Interpretationstext
- `subhead(text)` — blaue Sub-Überschrift innerhalb eines H3 (nicht im TOC, für Kennzahl-Labels)
- `datenquelle(text)` — grauer zentrierter „Quelle: …"-Marker unter Tabellen/Abbildungen

## 📝 Offene Erweiterungen im Scaffold (als Notizen markiert)

### FF1 (Kap. 4)
- **E5.1 Halbperioden-Vergleich** → 4.5.4 (Notizen + grafikFehlt)
- **E5.3 Asymmetrie-Test** → 4.5.5 (Notizen + grafikFehlt)
- **E5.4 Halblebensdauer** → Notiz in 4.1.1 nach 5-Punkt-Workflow
- Zusatz: deskriptive Statistik (phi1_mean, phi1_std, sigma_mean, sigma_std) → Info-Notiz an Tab. 4.1

### FF2 (Kap. 5)
- **E6.1 Lead-Lag** → 5.1.5 (Notiz + grafikFehlt Heatmap)
- **E6.2 Event-Heterogenität Sektor** → 5.2.5 (Notiz + grafikFehlt kleine Multiples)
- **E6.4 Korrelationsstabilität Teilperioden** → 5.5.1 (Notiz + grafikFehlt facettierte Heatmaps)
- **E6.5 Bonferroni α/42** → Notiz in 5.1.1
- Interpretation-H2 (5.3) mit 4 H3-Platzhaltern
- Fallbeispiele (🎯) in 5.2.3 (COVID) und 5.3.3 (GFC)

### FF3 (Kap. 6)
- **E7.1 Größen-Quintile** → 6.2.5 (Notiz + grafikFehlt Boxplot)
- **E7.2 Temporale Konsistenz / Übergangsmatrix** → 6.1.4 (Notiz + grafikFehlt Heatmap)
- **E7.4 Finanzsektor-Deep-Dive** → 6.4.4 (Notiz + grafikFehlt Overlay-Histogramm)
- **E7.5 Bonferroni α/7** → Notiz in 6.2.1
- Interpretation-H3 (6.1.5) + Platzhalter in 6.3.3, 6.4.3, 6.5
- Fallbeispiele (🎯) in 6.2.3 (Apple vs. Duke Energy) und 6.4.3 (JPMorgan vs. 3M)

## ⚠️ Offene Fixes F1–F5

| # | Problem | Ort (neu) | Status |
|---|---|---|---|
| F1 | ~197 kaputte Umlaute (ae/oe/ue) | Kap. 7 Diskussion | offen |
| F2 | Datenquelle: Compustat → EODHD Financial API | Kap. 1.3 | offen |
| F3 | TODO-Marker zu USGAAP vs. IFRS | Methodik (Kap. 3.x) | offen |
| F4 | Befund 4 doppelt | Kap. 5 (FF2) | offen |
| F5 | Cramér's V in FF2 muss raus (Stollhoff E11) | Kap. 5.1 | als Warnung in Kap.-Notiz — Text noch zu entfernen |

---

## 🕓 Originalabschnitt vom 21.04.2026 (folgt unten)

---

## ⭐ Einzige Quelle der Wahrheit

**→ [`Text/MASTER_REFERENZ.md`](Text/MASTER_REFERENZ.md)** ist ab jetzt **das** konsolidierte Dokument für:
- den aktuellen Stand jedes Kapitels (Ist/Soll-Matrix basierend auf PDF-Analyse)
- alle Prof-Absprachen (11.12.2024 Meeting, 14.03.2026 Mail, 26.03.2026 Meeting)
- das „Perfektes Kapitel"-Bewertungsraster (8 Kriterien aus Stollhoff-Feedback)
- die Quellenlandkarte (10 PDFs + 2 Lehrbücher vorhanden, 4 zu beschaffen)
- Gaps & Prioritäten P1–P5 mit Zeitplan bis 21.05.

Dieses Dokument (`COWORK_KONTEXT.md`) bleibt als **Session-Briefing** (Arbeits-Konventionen, Ordnerstruktur, Methodik-Fixpunkte, laufende Prioritäten-Schnellübersicht). Für den ganzheitlichen Thesis-Stand immer in MASTER_REFERENZ.md einsteigen.

**Weitere Living Briefings:**
- [`Text/FF1_UEBERSICHT.md`](Text/FF1_UEBERSICHT.md) — FF1-spezifische Navigation (Grafiken, CSVs, 4 Figurvorschläge)
- [`Text/GESAMTPLAN_APRIL_2026.md`](Text/GESAMTPLAN_APRIL_2026.md) + [`Text/PROJECT_STATUS.md`](Text/PROJECT_STATUS.md) — Zeitplan & Rollen
- [`Text/GLIEDERUNG_MASTERARBEIT.md`](Text/GLIEDERUNG_MASTERARBEIT.md) — 77 KB detaillierter Schreibplan pro Kapitel

---

## 🎯 Projekt-Kurzfassung

**Masterarbeit:** Zeitreihenbasierte Analyse der Dynamik von Finanzkennzahlen börsennotierter Unternehmen  
**Autor:** Tobias Mourier, TH Wildau  
**Abgabe:** 21. Mai 2026 — **30 Tage**  
**Betreuer:** Prof. Stollhoff (Methodik), Prof. Steglich (Finanzen/Interpretation)

**Kernmethode:** AR(1) auf ersten Differenzen, individuell pro Unternehmen (Mean-Group-Estimator)  
**Sample:** 932 US-Unternehmen, Q1/2000–Q4/2024, 7 Finanzkennzahlen  
**Zentraler Befund:** Drei-Schichten-Hierarchie der Mean-Reversion  

---

## 🧭 Arbeits-Konventionen (bestätigt 21.04.2026)

- **Führungsdokument für den aktuellen Schreibstand:** `Text/Text.pptx` (und als Reserve-PDF im gleichen Ordner). In der PPTX ist der zuletzt manuell geschriebene Text — **nicht** in Finale_Kapitel/.
- **`Text/` = Arbeitsdateien.** Entwürfe, Planung, Diskussionen, Übersichten, Prompts. Alles Lebende landet hier.
- **`Finale_Kapitel/` = AI-Rohfassung + finale Abbildungen.** Die .md-Dateien sind grobe, maschinell erstellte Entwürfe und müssen gemäß `ERWEITERUNGSPOTENZIALE.md` überarbeitet werden. Die `Kapitel_X_Grafiken/`-Unterordner enthalten fertige Publikations-Abbildungen.
- **DOCX-Dateien:** `Finale_Kapitel/Masterarbeit_Mourier.docx` (5,8 MB, 04.04.) und `Text/Masterarbeit Arbeitsdokument.docx` (25.03.) sind beide **nicht** der Master. Die eigentliche aktuelle Fassung lebt in der PPTX.
- **Cleanup-Status:** Bewusst aufgeschoben. Lockfiles, Backups, Kopien bleiben stehen bis Arbeit schreibgereift ist.
- **Ordner-Konsolidation `Text/` ↔ `Finale_Kapitel/`:** Wird **nicht** konsolidiert — die beiden Ordner haben unterschiedliche Zwecke (s.o.).

---

## 📁 Ordnerstruktur

```
Zeitreihenanalyse Finanzkennzahlen/
├── src/                          ← Python-Pipeline
│   ├── load_data.py
│   ├── ar_model.py               ← AR(1)-Schätzung
│   ├── classify.py               ← Quadrantenklassifikation
│   ├── external_validation.py    ← FF3
│   ├── company_profiles.py
│   ├── export_ff1_charts.py
│   └── robustness_samples.py
├── output/
│   ├── ar/
│   │   ├── ar_summary_by_ratio.csv     ← FF1 HAUPTERGEBNISSE (φ₁, σ pro Kennzahl)
│   │   ├── ar_features_all.csv         ← alle 6.521 Einzelschätzungen
│   │   ├── ar_summary_by_model_ratio.csv ← Robustheit (4 Varianten)
│   │   └── phi1_sigma_correlation.csv  ← Spearman φ₁×σ pro Kennzahl
│   ├── interdependence/
│   │   ├── corr_phi1.csv               ← FF2: 7×7 Korrelationsmatrix φ₁
│   │   ├── corr_sigma.csv              ← FF2: 7×7 Korrelationsmatrix σ
│   │   ├── pval_phi1.csv               ← p-Werte φ₁-Matrix
│   │   ├── pval_sigma.csv              ← p-Werte σ-Matrix
│   │   └── quadrant_crosstabs.csv      ← ALT (Cramér's V) — nicht mehr verwenden
│   ├── profiles/
│   │   ├── consistency_summary.csv     ← FF3: Konsistenz-Scores
│   │   ├── ff3_chi2_results.csv        ← FF3: Brancheneffekte χ²
│   │   ├── ff3_size_effects.csv        ← FF3: Größeneffekte Spearman
│   │   └── company_quadrant_profiles.csv
│   ├── clustering/
│   │   ├── kmeans_ar_dynamics_labels.csv   ← FF3: K-Means Ergebnisse
│   │   ├── kmeans_ar_dynamics_diagnostics.csv
│   │   └── quadrant_assignments.csv
│   ├── explore/
│   │   ├── peak_windows.csv            ← FF2: Event-Analyse Krisenquartale
│   │   └── volatility_scores.csv       ← FF2: Querschnittsvolatilität
│   ├── robustness/
│   │   ├── sample_comparison.csv       ← Stichprobenrobustheit (40Q/60Q/80Q/100Q)
│   │   └── financial_services.csv      ← Finanzsektor-Analyse
│   └── plots/                          ← bestehende Grafiken
├── Finale_Kapitel/                     ← ZIELDATEIEN (Markdown pro Kapitel)
│   ├── Kapitel_4_Methodik.md           ← weitgehend fertig
│   ├── Kapitel_5_FF1_Ergebnisse.md
│   ├── Kapitel_6_FF2_Interdependenzen.md
│   ├── Kapitel_7_FF3_Externe_Validierung.md
│   └── ...
├── generate_plots_v2.py                ← Grafik-Skript
└── analysis.ipynb                      ← Explorations-Notebook
```

---

## 📊 Zentrale Befunde (fixiert)

### FF1 — Drei-Schichten-Hierarchie

| Schicht | Kennzahl | φ₁ Median | σ Median | Signifikanzrate |
|---------|----------|-----------|----------|-----------------|
| Profitabilität | ROA | −0,43 | 0,017 | 92,2% |
| Profitabilität | ROE | −0,43 | 0,048 | ~88% |
| Profitabilität | EBIT-Marge | −0,43 | 0,062 | ~85% |
| Profitabilität | FCF-Marge | −0,46 | 0,165 | 90% |
| Liquidität | Current Ratio | −0,17 | — | 46% |
| Kapitalstruktur | Debt/Equity | −0,09 | — | 32% |
| Kapitalstruktur | EK-Quote | −0,04 | — | 19% |

**Robustheit:** Hierarchie stabil über alle 4 AR-Varianten und alle Stichprobengrößen (40Q–100Q, Abweichung <3% bei Profitabilität).

**Dimensions-Unabhängigkeit:** |ρ(φ₁, σ)| < 0,19 für Profitabilität; 0,19–0,24 für Bilanzstruktur.

### FF2 — Interdependenzen

**φ₁-Matrix (Korrekturgeschwindigkeit):**
- Profitabilitätsintern: ρ = 0,50–0,78 (ROA×ROE: 0,78; ROA×EBIT: 0,54; ROE×EBIT: 0,50)
- Alle 15 cross-kategorialen Paare: |ρ| < 0,10
- FCF als Sonderfall: φ₁-Kopplung zu buchhalterischen Kennzahlen nur ρ = 0,15–0,20

**σ-Matrix (Volatilitätskopplung) — fundamental anderes Muster:**
- ROE × D/E: ρ_σ = 0,82 (DuPont-Mechanik, formelbedingt)
- EBIT × FCF: ρ_σ = 0,78 (gemeinsamer Umsatznenner)
- EK-Quote als Brücke: σ-Korrelationen über alle 3 Schichten

**Event-Analyse (3 Krisen):**
- Dot-Com: 2000Q4–2002Q1 (3 Peaks)
- GFC: 2008Q4–2009Q3 (2009Q1: 6 von 7 Kennzahlen gleichzeitig)
- COVID: 2020Q1–2020Q4 (4 konsekutive Quartale, breitestes Event)

### FF3 — Externe Validierung

- **Konsistenz:** nur 1,2% vollständig konsistent über alle 7 Kennzahlen; schichtbasiert 97,6%
- **Branche:** χ² p < 0,001 für alle 7 Kennzahlen; Cramér's V = 0,18–0,29 (moderat)
- **Größe → σ:** Mitarbeiterzahl ρ bis −0,53 (FCF, Current Ratio); alle p < 0,001
- **Größe ↛ φ₁:** ROA ρ = −0,03 (p=0,34) — Korrekturmechanismus größenunabhängig
- **K-Means:** 81% stabil (Cluster 0), 19% hochvolatil (Cluster 1)
- **Finanzsektor:** Drei-Schichten-Hierarchie gilt auch dort; Current Ratio φ₁ = −0,41 vs. −0,17 Hauptanalyse

---

## 📋 Kapitelstatus & Gliederung

### Kap. 1 — Einleitung ❌ NICHT GESCHRIEBEN
*Schreiben erst wenn Kap. 2–8 als Entwurf stehen.*

```
1.1 Problemstellung
    - Einstiegsbeispiel: TAP vs. QCOM (gleicher ROA-φ₁, völlig verschiedene Unternehmen)
    - Warum Veränderungsdynamik statt Niveaus?
1.2 Forschungsfragen
    - FF1 (hypothesengeleitet): Systematische Dynamikunterschiede zwischen Kennzahlentypen
    - FF2 (explorativ): Interdependenzen + zeitliche Manifestation in Krisen
    - FF3 (hypothesengeleitet/explorativ gemischt): Externe Validierung
1.3 Aufbau der Arbeit
    - Kapitelübergänge explizit nennen
```

---

### Kap. 2 — Theoretische Grundlagen ⚠️ NOTIZEN VORHANDEN, TEXT FEHLT
*Stichpunkt-Listen in Kap. 2.2.3, 2.3.1, 2.3.3 vorhanden — müssen ausformuliert werden.*

```
2.1 Finanzkennzahlen und ihre ökonomische Bedeutung
    2.1.1 Die sieben Kennzahlen (Formeln + Definitionen)
    2.1.2 Drei Kategorien und ihre ökonomische Logik
          → Profitabilität: marktgetrieben, Output-Kennzahlen
          → Liquidität: hybrid
          → Kapitalstruktur: managementgesteuert, Input-Kennzahlen
          → Diese Dreiteilung = HYPOTHESE für FF1
    2.1.3 DuPont-Zerlegung
          → ROE = ROA × (1 + D/E) — erklärt ROE×D/E ρ_σ = 0,82 in FF2

2.2 Mean-Reversion in der Finanztheorie
    2.2.1 Das Konzept (Wettbewerb, Normalisierung)
    2.2.2 Niveaupersistenz vs. Veränderungskorrektur
          → Beispiel: EK-Quote φ₁,levels=0,93 aber φ₁,diff=−0,04
    2.2.3 Stationarität und die Wahl erster Differenzen [NOTIZEN VORHANDEN]
          → I(0)/I(1)/I(2), Hamilton (1994, Kap. 3)
          → Verweis auf 4.2.1 für Anwendung

2.3 Autoregressive Modelle
    2.3.1 Das AR(1)-Modell [NOTIZEN VORHANDEN]
          → Gleichung, φ₁-Interpretation, OLS, R², t-Test, Panel-Kontext
          → Mean-Group-Estimator (Pesaran & Smith 1995)
    2.3.2 Vier Modellvarianten (Übersichtstabelle)
    2.3.3 Warum AR(1) und nicht komplexere Modelle? [NOTIZEN VORHANDEN]
          → VAR: |ρ| < 0,10 cross-kategorial → kein Bedarf
          → GARCH: bedingte Varianz, nicht Mittelwert; 23–42% Konvergenz
          → Parsimonie-Prinzip

2.4 Quadrantenklassifikation als Typologierahmen
    2.4.1 Zwei Dimensionen, vier Dynamiktypen (Tabelle mit Labels)
    2.4.2 Median-Split: Begründung und Einschränkungen
          → MacCallum (2002): ~20% Infoverlust
          → Rucker (2015): OK wenn gering korreliert → empirisch geprüft
    2.4.3 Empirische Trennbarkeit der Dimensionen
          → Verweis auf Ergebnisse in 5.3.3
```

**Fehlende Literatur:** Hamilton (1994) oder Wooldridge (2012) — beschaffen!

---

### Kap. 3 — Stand der Forschung ❌ NICHT GESCHRIEBEN

```
3.1 Earnings Persistence und Mean-Reversion
    3.1.1 Die klassische Perspektive
          → Sloan (1996): Accruals vs. Cashflow-Persistenz [FEHLT — BESCHAFFEN]
          → Dechow (1994): Accrual-Timing
          → Dichev & Tang (2009): AR(1) auf Earnings — HAUPTBENCHMARK
          → Fama & French (2000): Mean-Reversion Profitabilität [FEHLT — BESCHAFFEN]
    3.1.2 Was die Literatur nicht leistet
          → Nur Niveaupersistenz, kein systematischer Kennzahlen-Vergleich
          → Kein Veränderungsperspektive über 7 Kennzahlen

3.2 Firmengröße und Kennzahlen-Dynamik
    3.2.1 Der Größeneffekt in der Finanzforschung
          → Fama & French (1992): Size-Faktor auf Renditen
    3.2.2 Empirische Evidenz: Größe erklärt Volatilität, nicht Korrekturgeschwindigkeit
          → Eigener Befund: ρ bis −0,53 für σ, aber ρ ≈ 0 für φ₁

3.3 Brancheneffekte und mechanische Kopplungen
    3.3.1 Branchenspezifische Dynamik
          → Eljelly (2004): Liquiditäts-Profitabilitäts-Trade-off
    3.3.2 Mechanische Kopplungen: Der Leverage-Effekt
          → Christie (1982) + Nissim & Penman (2001): DuPont

3.4 Cluster-Analyse und Unternehmensklassifikation
    3.4.1 Bestehende Ansätze: Dzuba & Krylov (2021) auf Niveaus
    3.4.2 Abgrenzung: eigene Arbeit clustert Dynamikparameter (φ₁, σ)

3.5 Forschungslücke und Beitrag dieser Arbeit
    3.5.1 Synthese der drei Lücken
    3.5.2 Beitrag: 3 Punkte (systematischer Vergleich, Veränderungsperspektive, Quadrant)
```

---

### Kap. 4 — Methodik ✅ WEITGEHEND FERTIG
*Korrekturen noch nötig:*
- [ ] Interne Frage "Pesaran macht der Ökonomische sachen?" aus 4.2.3 entfernen → Antwort: technisch-ökonometrisch; Ökonomiebezug kommt vom Autor
- [ ] Kap. 6.2.4 im Dokument noch als "Cramér's V" bezeichnet → muss weg (FF2-Methodik)

---

### Kap. 5 — FF1: Systematische Dynamikmuster ⚠️ GLIEDERUNG STEHT, TEXT FEHLT
*CSV: `output/ar/ar_summary_by_ratio.csv` + `ar_features_all.csv` + `ar_summary_by_model_ratio.csv`*

```
5.1 Die Drei-Schichten-Hierarchie im Überblick
    5.1.1 Modellgüte als Einstieg [NOTIZ VORHANDEN — ausformulieren]
          → R²-Verteilung über alle 6.521 Schätzungen
          → Signifikanzraten gesamt + pro Kennzahl
    5.1.2 Die drei Schichten
          → Tabelle: φ₁-Mediane, IQR, Signifikanzrate, R²-Median pro Kennzahl
          → Visualisierung: Boxplot φ₁-Verteilungen der 7 Kennzahlen
    5.1.3 Verbindung zur Theorie
          → HYPOTHESENGELEITET: Marktexposition → Korrekturgeschwindigkeit
          → Dichev & Tang (2009) Vergleich: exakte Zahlen nebeneinander

5.2 Detailanalyse pro Kennzahl
    5.2.1 ROA als Leitkennzahl
          → IQR [−0,50; −0,33], branchenübergreifendes Muster
          → Auch am 95. Pz. noch negatives φ₁ (−0,16)
    5.2.2 ROE — Leverage-Verstärkung
          → φ₁ strukturell nahe ROA (gemeinsame operative Treiber, DuPont)
          → aber σ deutlich höher (Leverage-Verstärkung)
    5.2.3 EBIT-Marge — Operative Margendynamik
    5.2.4 FCF-Marge — Stärkste Veränderungskorrektur
          → φ₁ = −0,46 (stärkste Korrektur)
          → ABER schwächste φ₁-Kopplung zu buchhalterischen Kennzahlen (ρ=0,15–0,20)
          → Dechow (1994): Accrual-Timing ändert Korrekturstruktur, nicht Stärke
    5.2.5 Current Ratio — Die Übergangszone
          → φ₁ = −0,17: hybrid zwischen Profitabilität und Kapitalstruktur
          → Signifikanzrate 46% (deutlich niedriger als Profitabilität)
    5.2.6 Kapitalstruktur — Kein AR-Signal auf Differenzen
          → φ₁,diff ≈ 0 ABER φ₁,levels = 0,87–0,93
          → Diskrete Managemententscheidungen, kein quartalsweiser Feedback

5.3 Robustheit
    5.3.1 Modellvarianten
          → Tabelle: φ₁-Mediane unter diff1/levels/AR(2)/diff4
          → Rangordnung stabil — kein Artefakt der Transformationswahl
          ⚠️ CSV: ar_summary_by_model_ratio.csv
    5.3.2 Stichprobenrobustheit [EIN ABSATZ VORHANDEN — erweitern]
          → 932/1.231/1.855/2.356 Unternehmen
          → Profitabilität <3% Abweichung, Kapitalstruktur größere relative Schwankung
          ⚠️ CSV: robustness/sample_comparison.csv
    5.3.3 Empirische Trennbarkeit der Quadrantendimensionen [NOTIZ VORHANDEN]
          → Spearman-Tabelle φ₁×σ pro Kennzahl
          → |ρ| < 0,19 Profitabilität; 0,19–0,24 Bilanzstruktur
          → χ²-Test auf Gleichverteilung
          → Abbildung 4.1 (Scatterplot ROA) — ZWEITE MEDIANLINIE FEHLT IN GRAFIK
          ⚠️ CSV: ar/phi1_sigma_correlation.csv

5.4 Sektorale Heterogenität [EXPLORATIV]
    5.4.1 Überblick + Drei Sektorgruppen
          → Gruppe A Korrektiv-Volatil: Comm.Services 38%, Energy 39%, Real Estate 44%
          → Gruppe B Persistent-Volatil: Technology 32%, Basic Materials 31%
          → Gruppe C Stabil: Consumer Defensive 64%, Industrials 64%
    5.4.2 Geschäftsmodell-Interpretationen
          → Comm. Services φ₁=−0,49: hohe Fixkosten + schwankende Erlöse
          → Basic Materials φ₁=−0,37: Rohstoffzyklen über mehrere Quartale
          → Utilities D/E φ₁=−0,17 vs. −0,09 gesamt: regulatorische Zielwerte
          → Real Estate CR φ₁=−0,34 vs. −0,17 gesamt: REIT-Refinanzierungszyklen
          ⚠️ CSV: output/plots/sectors/

5.5 Zusammenfassung FF1 + Überleitung FF2
```

---

### Kap. 6 — FF2: Interdependenzen ⚠️ GLIEDERUNG STEHT, TEXT FEHLT
*CSV: `output/interdependence/` + `output/explore/`*

```
6.1 Methodik
    6.1.1 Querschnittsanalyse
          → NUR Spearman auf metrischen φ₁- und σ-Werten
          → KEIN Cramér's V (Stollhoff: metrische Daten metrisch testen)
          → Bonferroni-Handling: Option A (ohne Korrektur, ehrliche Einordnung)
          → Bei 21 Tests ~1 zufällig signifikantes Ergebnis bei α=5%
    6.1.2 Event-Analyse
          → Peak wenn ≥3 von 7 Kennzahlen gleichzeitig >90. Pz. Querschnittsvolatilität
          → Mann-Whitney U + Kruskal-Wallis für Quadranten-Reaktionsvergleiche

6.2 Querschnittliche Interdependenz
    6.2.1 Die φ₁-Korrelationsmatrix
          → Blockstruktur: intern 0,50–0,78 vs. cross |ρ| < 0,10
          → Scatterplots: ROA×ROE (ρ=0,78), ROA×EBIT (ρ=0,54)
          → HYPOTHESENGELEITET bestätigt
          ⚠️ CSV: corr_phi1.csv, pval_phi1.csv
    6.2.2 Die σ-Korrelationsmatrix — ein anderes Muster
          → ROE×D/E ρ_σ=0,82: mechanisch (DuPont), nicht ökonomisch
          → EBIT×FCF ρ_σ=0,78: gemeinsamer Umsatznenner
          → Scatterplot: ROE-σ vs. D/E-σ
          ⚠️ CSV: corr_sigma.csv, pval_sigma.csv
    6.2.3 φ₁ versus σ: Zwei verschiedene Informationsdimensionen
          → ROE×D/E: ρ_φ₁=0,07 aber ρ_σ=0,82 — schärfster Kontrast
          → σ = gemeinsamer Expositionsfaktor; φ₁ = kennzahlenspezifischer Strukturparameter
    6.2.4 ~~Quadrantenüberschneidungen (Cramér's V)~~ → ENTFERNEN
          → Stattdessen: kurze Zusammenfassung der Hauptbefunde aus 6.2.1–6.2.3

6.3 Zeitliche Manifestation: Event-Analyse [EXPLORATIV]
    6.3.1 Identifizierte Peak-Windows
          → Dot-Com 2001Q1, GFC 2009Q1 (stärkstes Event), COVID 2020Q2
          ⚠️ CSV: explore/peak_windows.csv
    6.3.2 Quadranten-Reaktionen auf Events
          → Dot-Com: Korrektiv-Stabil +0,0021 vs. Persistent-Volatil −0,0008
          → COVID: alle negativ, volatile Quadranten bis 3× stärker
          ⚠️ CSV: explore/volatility_scores.csv
    6.3.3 Cross-Ratio-Reaktionsmuster
          → Welche Kennzahlen reagieren zuerst/stärker?
          ⚠️ Grafik: output/plots/ff2_quadrant_reactions.png

6.4 Zusammenfassung FF2 + Überleitung FF3
```

---

### Kap. 7 — FF3: Externe Validierung ⚠️ GLIEDERUNG STEHT, TEXT FEHLT
*CSV: `output/profiles/` + `output/clustering/`*

```
7.1 Das Konsistenzproblem
    7.1.1 Ausgangslage: Ist ein Unternehmen dauerhaft "korrektiv"?
    7.1.2 Konsistenz-Scores
    7.1.3 Tabelle 7.1: Konsistenz der Quadrantenzuordnung
          → Vollständig konsistent: 1,2% — Schichtbasiert konsistent: 97,6%
          ⚠️ CSV: profiles/consistency_summary.csv

7.2 Brancheneffekte: χ²-Tests
    7.2.1 Ergebnisse
          → p < 0,001 für alle 7 Kennzahlen
    7.2.2 Tabelle 7.2: χ²-Tests Sektor × Quadrant
          → Cramér's V = 0,18 (D/E) bis 0,29 (Current Ratio)
          → Hier ist Cramér's V KORREKT (Sektor ist kategorial)
          ⚠️ CSV: profiles/ff3_chi2_results.csv
    7.2.3 Interpretation
          → HYPOTHESENGELEITET: Branche erklärt Quadrant (moderat, nicht vollständig)

7.3 Größeneffekte
    7.3.1 Die Asymmetrie des Größeneffekts
          → HYPOTHESENGELEITET: Größe → σ (ρ bis −0,53) ✓
          → EXPLORATIV: Größe ↛ φ₁ (ρ ≈ 0) — überraschend
          → Mitarbeiterzahl > Marktkapitalisierung als Prädiktor
          → Fama & French (1992) Analogie: Size-Effekt auf Renditen → hier auf σ
          ⚠️ CSV: profiles/ff3_size_effects.csv

7.4 K-Means als Robustheitscheck
    7.4.1 Methodik und Ergebnisse
          → k=2, 14 Features (7×φ₁ + 7×σ)
    7.4.2 Tabelle 7.3: K-Means-Cluster-Profile
          → Cluster 0 (81%, 10.616 MA Median): stabile Mehrheit
          → Cluster 1 (19%, 5.050 MA): hochvolatil
          → D/E σ-Faktor 18 zwischen Clustern
          ⚠️ CSV: clustering/kmeans_ar_dynamics_labels.csv + diagnostics
    7.4.3 Interpretation
    7.4.4 Sektorale Zusammensetzung
          → Healthcare 37% in Cluster 1, Energy 31%; Utilities 10%, Industrials 11%
    7.4.5 Methodische Implikation: bestätigt Median-Split-Klassifikation

7.5 Financial Services: Regulatorische Mean-Reversion
    7.5.1 Vergleich mit der Hauptanalyse
    7.5.2 Tabelle 7.4: φ₁-Mediane Hauptanalyse vs. Financial Services
          → ROA/ROE identisch −0,43; CR −0,41 vs. −0,17; D/E −0,20 vs. −0,09
          ⚠️ CSV: robustness/financial_services.csv
    7.5.3 Interpretation
          → Regulatorische Zielwerte → stärkere Mean-Reversion in Bilanzstruktur
          → Drei-Schichten-Hierarchie gilt auch im Finanzsektor

7.6 Zusammenfassung FF3 + Überleitung Diskussion
```

---

### Kap. 8 — Diskussion ❌ NICHT GESCHRIEBEN
*Stollhoff: "Interpretation ist das, was noch fehlt." Steglich bewertet das besonders.*

```
8.1 Ökonomische Interpretation der Befunde
    8.1.1 Warum eine Drei-Schichten-Hierarchie?
          → Marktexposition: Output-Kennzahlen → wettbewerbsgetriebener Korrekturmechanismus
          → Input-Kennzahlen → diskrete Managemententscheidungen
    8.1.2 Geschäftsmodell und sektorale Dynamikmuster
          → 5+ Sektoren mit Geschäftsmodell-Bezug
          → Technology: M&A definiert neues Normal → kein Korrekturimpuls
    8.1.3 Die zwei Dimensionen als unterschiedliche Konstrukte
          → φ₁ = Struktur des Geschäftsmodells (Wie temporär sind Veränderungen?)
          → σ = Expositionsmaß (Wie stark schwankt es?)
          → Operationale Diversifikation glättet σ, nicht φ₁

8.2 Einordnung in die Literatur
    8.2.1 Dichev & Tang (2009): Bestätigung + Erweiterung auf 7 Kennzahlen
          → Exakte Zahlen nebeneinanderstellen (Levels-φ₁ nicht vergleichbar!)
    8.2.2 Fairfield & Yohn (2001): Differenzen informativer als Niveaus bestätigt
    8.2.3 Fama & French (1992): Size-Effekt neu interpretiert (auf σ statt Renditen)
    8.2.4 Dechow (1994): FCF-Sonderfall erklärt
    8.2.5 Abgrenzung zu nicht verwendeten Methoden (VAR, GARCH)

8.3 Limitationen [EHRLICH — Stollhoff-Punkt]
    8.3.1 Median-Split: dreifach adressiert (K-Means, metrische Werte, Tercile verworfen)
    8.3.2 Survivorship Bias: 77% exkludiert; Profitabilität <3% robust
    8.3.3 Stationaritätsannahme und zeitliche Homogenität
    8.3.4 Einheitliche Transformation: bewusster Trade-off Vergleichbarkeit > Optimalität
    8.3.5 Kausalität: deskriptiv, kein Granger eingesetzt
    8.3.6 US-Fokus: GAAP/IFRS, Bilanzierungsspielräume → Mean-Reversion aus Geschäft oder Accounting?

8.4 Praktische Implikationen (kurz halten)
    → Analysten, Portfoliomanagement, Kreditanalyse
```

---

### Kap. 9 — Fazit und Ausblick ❌ NICHT GESCHRIEBEN
*Schreiben nach Kap. 8.*

```
9.1 Zusammenfassung der Ergebnisse
    → Je 1 Absatz pro FF (max. 5 Sätze)

9.2 Wissenschaftlicher Beitrag
    → (1) Systematischer 7-Kennzahlen-Vergleich mit einheitlicher Methode
    → (2) Veränderungsperspektive als eigenständiges Analysekonzept
    → (3) Quadrantenklassifikation extern validiert

9.3 Ausblick
    → Rolling-AR (Strukturbrüche über 25 Jahre)
    → Internationale Replikation — EU-Daten bereits vorhanden (für Verteidigung!)
    → Machine-Learning-Klassifikation
    → Granularere Saisonalitätsanalyse
```

---

## 🔑 Methodische Fixpunkte (nicht mehr ändern)

| Entscheidung | Stand | Begründung |
|---|---|---|
| AR(1) auf ersten Differenzen | FIXIERT | ex ante, kein selektiver Modellwechsel |
| Individuelle OLS pro Unternehmen | FIXIERT | Mean-Group-Estimator, heterogene Slopes |
| Cramér's V in FF2 | ENTFERNT | metrische Daten → Spearman |
| Cramér's V in FF3 (Sektor×Quadrant) | BLEIBT | Sektor ist kategorial → χ² korrekt |
| Monte-Carlo-Benchmark | ENTFERNT | Stollhoff: rausnehmen |
| Europäische Daten | NICHT IN ARBEIT | für mündliche Verteidigung aufheben |
| Bonferroni | Option A | ohne Korrektur, aber ehrliche Einordnung |

---

## 📌 Aktuelle Prioritäten

*Für den ausführlichen Zeitplan → MASTER_REFERENZ.md §5 (P1–P5). Hier nur Session-Kurzsicht.*

**Stand: 21. April 2026 (nach Session „Master-Referenz-Konsolidierung")** · 30 Tage bis Abgabe

**P1 — Blockierer diese Woche (21.–27.04.):**
1. [ ] Kap. 4 Restpunkte (7 Items, s. MASTER_REFERENZ §2 Kap. 4): TODO-Note 4.2.3, Cramér-V-Hinweis 4.5, Tab. 4.3 Farbe/Spalten, Abb. 4.1 zweite Medianlinie, Bonferroni α/42 vs. α/7, Hamilton/Wooldridge-Referenzen, Review-v2-Issues.
2. [ ] Kap. 6.2.4 „Cramér's V" aus PDF/PPTX entfernen → Spearman-Zusammenfassung.
3. [ ] Notebook 02.3/02.4 & METHODIK_DISKUSSION.md: Cramér-V- und Monte-Carlo-Reste bereinigen.
4. [ ] Literatur beschaffen: Sloan (1996), Fama & French (2000), Comin & Philippon (2006), Penman-Lehrbuch.

**P2 — Kernschreibphase (21.04.–04.05.):**
5. [ ] Kap. 2 Theorie (4–5 Tage) — Hamilton / Wooldridge / Pesaran & Smith einarbeiten; Kernpunkt 2.2 Niveaus ↔ Differenzen.
6. [ ] Kap. 3 Forschungsstand (3–4 Tage) — Literatureinordnung entlang 3.1–3.5.
7. [ ] Kap. 5 FF1 konsolidieren (4–5 Tage) — Rohtext + Grafiken + Interpretation; FF1_UEBERSICHT.md als Navigationskarte; 4 neue Figurvorschläge (abb_5_1b σ-Boxplots, 5_2b Literatur-Benchmark, 5_7 φ₁×σ Scatter, 5_5b σ-Sektor-Heatmap).
8. [ ] Kap. 6 FF2 konsolidieren (3–4 Tage) — Spearman-Narrativ, Event-Analyse.
9. [ ] Kap. 7 FF3 konsolidieren (3–4 Tage) — Konsistenz, χ², Größe, K-Means, FinServ.

**P3 — Einordnung & Abschluss (05.05.–14.05.):**
10. [ ] Kap. 8 Diskussion (4–5 Tage) — IFRS/US-GAAP, Survivorship, Multiple Testing, Kausalität, Elefanten/Wolken.
11. [ ] Kap. 9 Fazit (1–2 Tage).
12. [ ] Kap. 1 Einleitung (1–2 Tage) — zum Schluss, mit TAP-vs-QCOM-Einstieg.

**P4 — Feinschliff (15.05.–18.05.):** Querverweise, Grafiken-Druckqualität, Verzeichnisse, Korrekturlesen.

**Puffer:** 19.–21.05. · **Abgabe:** 21.05.

**P5 — nach Abgabe:** Verteidigungsbonus (Europa-Daten, MC), Artikel mit Stollhoff.

**Als nächstes in Cowork:** P1-Items abschließen (Kap. 4 Restpunkte + Cramér-V-Bereinigung) oder Kap. 2 Theorie-Schreiben starten.

---

## ⚠️ Offene Fragen / Unsicherheiten

- [ ] Pesaran & Yang (2024) vs. Pesaran & Smith (1995) — welche Quelle für individuelle OLS?  
  *Antwort: Pesaran & Smith (1995) für Mean-Group-Estimator-Konzept; Pesaran & Yang (2024) für AR(1)-spezifischen Nachweis*
- [ ] Abbildung 4.1: Scatterplot ROA — zweite Medianlinie fehlt noch in generate_plots_v2.py
- [ ] Kap. 7.4 K-Means: Übereinstimmungsquote mit Quadranten noch nicht berechnet/dokumentiert

---

*Ende COWORK_KONTEXT.md — wird laufend ergänzt*
