# MASTER_REFERENZ — Masterarbeit Tobias Mourier

> **Einzige Quelle der Wahrheit** für Schreibphase. Konsolidiert: aktueller Stand (PDF/PPTX), Prof-Absprachen, „Perfektes Kapitel"-Kriterien, Quellenlandkarte, Gaps & Prioritäten.
> **Stand:** 2026-04-21 | **Abgabe:** 2026-05-21 (in 30 Tagen) | **Betreuer:** Prof. Stollhoff (Methodik, Erstgutachter) · Prof. Steglich (BWL, Zweitgutachter)

---

## 0. Executive Summary

**Kern der Arbeit.** AR(1) auf ersten Differenzen (ΔY) für 7 Finanzkennzahlen über 932 US-Unternehmen (S&P Composite 1500, Q1/2000–Q4/2024). Zwei Dimensionen pro Unternehmen-Ratio-Paar: φ₁ (Mean-Reversion der Veränderungen) und σ(ΔY) (Änderungsvolatilität). Quadrantenklassifikation via Median-Split. Drei Forschungsfragen adressieren: systematische Muster (FF1), Interdependenz (FF2), externe Validierung (FF3).

**Zentrales Ergebnis.** Drei-Schichten-Hierarchie: Profitabilität (φ₁ ≈ −0,43 bis −0,46) > Liquidität (−0,17) > Kapitalstruktur (−0,04 bis −0,09). Robust über 4 Modellvarianten und 4 Stichprobengrößen. Ökonomische Deutung: marktgetrieben vs. managementgesteuert.

**Stand heute (21.04.2026).**
- Code & Analysen: **fertig** (Pipeline, CSVs, Plots, Dashboard v4).
- Kap. 4 Methodik: **geschrieben** im Arbeitsdokument (Text/Text.pptx), inkl. Prof-Feedback-Einbau bis auf 4 konkrete Restpunkte.
- Kap. 5 (FF1): **Rohtext vorhanden** in Finale_Kapitel/Kapitel_5_FF1_Ergebnisse.md; Grafikeinbindung & Feinschliff offen.
- Kap. 6/7 (FF2/FF3): Ergebnisse als Text in output/FF2_/FF3_*.md aufbereitet; **Konsolidierung im Arbeitsdokument offen**.
- Kap. 1, 2, 3, 8, 9: **nicht geschrieben**, Gliederung und Quellenreferenzen in GLIEDERUNG_MASTERARBEIT.md (77 KB) detailliert vorbereitet.
- Literatur: 10 Kernquellen als PDFs vorhanden; 3 Kernartikel und Penman-Lehrbuch noch zu beschaffen.

**Kritischer Pfad.** (1) Kap. 4 Restpunkte schließen, (2) Theoriekapitel 2 & 3 schreiben (Stollhoff-Feedback: Interpretation + Quelleneinbettung = Hauptbewertungskriterium), (3) Ergebniskapitel 5–7 fertigstellen, (4) Diskussion (IFRS/US-GAAP, Limitationen, Bewertungsspielräume), (5) Fazit, (6) Einleitung, (7) Feinschliff. 30 Tage. Puffer 19.–21.05.

---

## 1. Prof-Absprachen — konsolidiert

### 1.1 Meeting 11.12.2024 (Stollhoff + Steglich) — Erste Weichenstellung

| Thema | Entscheidung |
|---|---|
| Methodik | **ARIMA/GARCH + einfaches Clustering** (nicht Random Forest, SHAP, ML) — Begründung: im Studium gelernt |
| Datenquelle | **FMP API** (später: EODHD), nicht WRDS (TH Wildau keine Lizenz) |
| Fokus | **Interpretation > Algorithmen-Vergleiche** |
| Betreuung | Stollhoff = Erstgutachter (Methodik), Steglich = Zweitgutachter (BWL) |
| Clustering | **Werkzeug**, kein Forschungsbeitrag |

### 1.2 Mail Prof. Stollhoff 14.03.2026 — Zwischenstand Woche 7

- ✅ Datenaufbereitung: keine Kritik.
- ✅ FF1 „klingt interessant".
- ✅ Survivorship-Bias-Ansatz (variable Stichproben 40/60/80/100Q) genehmigt.
- ⏳ **US-GAAP vs. IFRS**: Methodik-OK, Limitation-Diskussion nötig → Antwort Steglich steht aus.
- **Kernforderung**: Begründung der Modellwahl stärken + Alternativen (AR(p), Saisonalität, Levels) diskutieren. → daraus entstand der Vier-Varianten-Robustheitscheck.

### 1.3 Meeting 26.03.2026 (Stollhoff alleine, Steglich krank) — Kurskorrektur

**Tenor:** Umfang reicht, Methodik ist komplex genug, **nichts mehr hinzufügen**. Jetzt ist nur noch Schreibphase. **Interpretation = Hauptbewertungskriterium**.

| Entscheidung | Begründung Stollhoff (wörtlich / sinngemäß) | Status |
|---|---|---|
| **Monte-Carlo-Benchmark RAUS** | „−0,751 wirkt mathematisch unplausibel. Wenn es falsch ist: Abzug. Wenn es fehlt: kein Abzug." | ✅ aus Kap. 4 entfernt; ⚠️ Notebook & METHODIK_DISKUSSION.md noch anpassen |
| **Cramér's V RAUS für FF2** → Spearman | „Nehmen Sie einfach Biermin-Rangkorrelation. Rangkorrelation geht immer, ohne Normalverteilungstest." | ✅ Kap. 4.5 Text entfernt; ⚠️ Kap. 6.2.4 im PDF noch präsent, Notebook 02.3/02.4 nutzt noch Cramér's V |
| **Cramér's V BLEIBT für FF3** | Dort korrekt, weil Daten bereits diskret (Sektor × Quadrant). | ✅ unverändert |
| **Europa-Daten RAUS** | „Sie müssen nicht eine zusätzliche Datenquelle nehmen." (geparkt für Verteidigung) | ✅ geparkt |
| **Keine neuen Kennzahlen** | „Reicht aus." Vergleich mit Dichev & Tang nur über FCF-Marge in Diskussion. | ✅ entschieden |
| **Mehrfachtesten** | Bonferroni (α/n) oder raw p + Caveat in Diskussion. Beides vertretbar. | ⏳ durchgängig beim Schreiben |
| **Hypothesen trennen** | Aus Literatur abgeleitet vs. explorativ gefunden — klar kennzeichnen („Wolken & Elefanten"). | ⏳ durchgängig beim Schreiben |
| **Keine Granger-Kausalität/VAR** | Cross-kategoriale φ-Korrelationen < 0,10 → VAR nicht informativ. | ✅ begründet, raus |
| **Keine Fama-French-Regression** | Scope-Begrenzung. | ✅ raus |
| **USGAAP vs. IFRS** | In Diskussionskapitel (Bewertungsspielräume, Management-Anreize) + Limitation. | ⏳ Kap. 8 |
| **Artikel-Angebot** | Stollhoff bietet Zusammenarbeit nach Abgabe für Publikation an. | 🎯 optional nach Abgabe |
| **Verteidigung** | Für Note Richtung 1,0: „noch ein, zwei Folien mit Sachen, die nach Abgabe gerechnet wurden" (z. B. Europa-Daten, MC) — macht sich gut. | 📌 nach Abgabe |
| **Zeitplan** | „Rechnen Sie 2–3 Wochen rein fürs Schreiben und Fertigstellen." | ⏰ Puffer ab ~04.05. |

### 1.4 Was Stollhoff durchgehend beim Schreiben erwartet

Aus dem Meeting 26.03. ergibt sich ein **Bewertungsraster**, das für jedes Kapitel gilt:

1. **Jede Zahl braucht eine ökonomische Erklärung** (WARUM, nicht nur WAS).
2. **Literaturvergleich für jeden zentralen Befund** (Sloan, Fama-French 2000, Dichev-Tang, Nissim-Penman, Christie).
3. **Exploratives klar als solches kennzeichnen** („Muster gefunden, Hypothese war offen").
4. **Nichts schreiben, was nicht verstanden wurde** — „dann lasse ich es lieber weg".
5. **Roter Faden** — der Leser darf nie denken: „Warum erzählt er mir das jetzt?"
6. **Großer Bogen** — Steglich will aus Kennzahlen eine BWL-Interpretation lesen.

---

## 2. Kapitelweise Ist/Soll-Matrix

Für jedes Kapitel: **aktueller Stand** (im PDF/PPTX), **verfügbare Vorarbeiten** (Dateien im Projekt), **Prof-Anforderungen**, **Kriterien „perfekt"**.

### Kap. 1 — Einleitung (2–3 Seiten) · Stand: **leer**

- **Stand PDF:** nur Überschriftenstruktur (1.1 Problemstellung, 1.2 Forschungsfragen, 1.3 Aufbau).
- **Vorarbeit:** GLIEDERUNG_MASTERARBEIT.md (detaillierter Schreibplan, inkl. TAP-vs-QCOM-Einstiegsbeispiel).
- **Zeitpunkt:** zum Schluss schreiben, wenn Kap. 2–9 stehen.
- **Kriterien:** konkretes Einstiegsbeispiel · exakte Forschungsfragen-Formulierung · expliziter Aufbau-Fahrplan.

### Kap. 2 — Theoretische Grundlagen (8–10 Seiten) · Stand: **Skelett + Notizen**

- **Stand PDF:** Überschriften komplett, Füllnotizen in 2.2.3 (Stationarität), 2.3.1 (AR(1), inkl. Mean-Group-Estimator Pesaran & Smith), 2.3.3 (Warum AR(1) — Parsimonie-Argument).
- **Vorarbeit:** GLIEDERUNG_MASTERARBEIT.md mit sehr detailliertem Schreibplan pro Abschnitt; METHODIK_DISKUSSION.md (24 KB) mit Uniformitätsargument.
- **Quellen:**
  - 2.1 Kennzahlen → Nissim & Penman (2001), Penman-Lehrbuch *(zu beschaffen)*.
  - 2.2 Mean-Reversion → Dichev & Tang (2009), Fairfield & Yohn (2001), Hamilton Kap. 3 ✅ (vorhanden).
  - 2.3 AR-Modelle → Hamilton Kap. 3.2–3.5 ✅, Wooldridge Kap. 18 ✅, Pesaran & Smith (1995).
  - 2.4 Quadranten → Rucker et al. (2015) für Median-Split-Zulässigkeit.
- **Offene Recherche-Aufgabe:** „Ep"-Quelle aus NotebookLM identifizieren.
- **Prof-Anker:** Kernpunkt 2.2 = **Niveaus vs. Differenzen** — theoretisch motivieren, warum beide Perspektiven zusammen das volle Bild ergeben (Stollhoff-Mail 14.03.).

### Kap. 3 — Stand der Forschung (6–8 Seiten) · Stand: **leer, Literatur vorhanden**

- **Stand PDF:** nur Skelett.
- **Vorarbeit:** GLIEDERUNG_MASTERARBEIT.md; 10 PDFs vorhanden.
- **Quellen pro Abschnitt** (nach PROJECT_STATUS):
  - 3.1 Earnings-Persistence: Sloan (1996) *(zu beschaffen)*, Fama & French (2000) *(zu beschaffen)*, Dichev & Tang (2009) ✅.
  - 3.2 Volatilität / Krisen: Comin & Philippon (2006) *(zu beschaffen)*, Christie (1982) ✅.
  - 3.3 Bilanzstruktur: Eljelly (2004) ✅, Love & Zicchino (2006) ✅ (als VAR-Gegenargument).
  - 3.4 Clustering-Referenzen: Dzuba & Krylov (2021) ✅.
  - 3.5 Lücke + Beitrag: abgeleitet aus 3.1–3.4.

### Kap. 4 — Methodik (10–12 Seiten) · Stand: **~85 % fertig, 4 Restpunkte**

- **Stand PDF (S. 38–59):** Kap. 4.1 Datengrundlage, 4.2 Modellspezifikation (OLS + AR(1) auf ΔY), 4.3 Quadrantenklassifikation, 4.4 Robustheitsdesign (4 Varianten, 4 Stichproben, Financial Services), 4.5 Statistische Auswertungsstrategie. Monte-Carlo entfernt, Cramér's V aus FF2 entfernt.
- **Vorarbeit:** METHODIK_DISKUSSION.md (24 KB), METHODIKENTSCHEIDUNGEN_TIMELINE.md (E1–E12), Methodik_Querschnitt.md (7 KB).
- **Restpunkte (aus GESAMTPLAN Phase 1):**
  - [ ] S. 46 (4.2.3): interne TODO-Note „Pesaran macht der Ökonomische sachen, oder ist das rein technisch?" entfernen → formulieren: Pesaran & Smith als ökonometrisches Heterogenitätsargument.
  - [ ] S. 56 (4.5): Note „Finalisierung dieses Abschnitts nach Kap. 5, 6 und 7" + „((Cramér's V??))" entfernen.
  - [ ] 10 Issues aus Review v2 (TODO-Notes, Grammatik, T=98/99-Korrektur).
  - [ ] Abbildung 4.1 (Quadrantenklassifikation ROA): zweite Median-Linie ergänzen.
  - [ ] Tabelle 4.3: rote Zeilenfarbe (EE0000) auf Schwarz; auf 3 Spalten reduzieren (Kennzahl, Spearman ρ, Signifikanz).
  - [ ] Bonferroni präzisieren: α/42 für FF2 (21 Paare × 2 Matrizen), α/7 für FF3 χ²-Tests.
  - [ ] Lehrbuch-Referenzen einfügen: Hamilton bei Stationarität (4.2 Schritt 1), Wooldridge bei AR-Herleitung (4.2 Schritt 2).

### Kap. 5 — FF1 Ergebnisse (12–15 Seiten) · Stand: **Rohtext vorhanden, keine Grafiken eingebunden**

- **Stand PDF (S. 60–79):** Überschriften komplett. Substantiell: S. 62 (5.1.1 Hauptergebnis-Notiz zur R²/Signifikanz-Darstellung), S. 73 (5.3.1 Tabelle Modellvarianten), S. 74–77 (5.3.3/5.4/5.4.1 mit viel eingefügtem Material aus 4.3.3/4.4.3/4.4.4 als Schreibmaterial).
- **Vorarbeit:**
  - `Finale_Kapitel/Kapitel_5_FF1_Ergebnisse.md` (170 Zeilen AI-Rohtext, inkl. 6 Figurverweise, Tab. 5.1, Drei-Schichten-Hierarchie-Exposé).
  - `output/FF1_Interpretation_AR1_Diffs.md` (38 KB, sehr detaillierte Interpretation mit Sektor-Tabellen φ₁ und σ).
  - `output/FF1_Ergebnisse.docx` (1,14 MB, 15 eingebettete Plots).
  - `Text/FF1_UEBERSICHT.md` (12,7 KB, Grafik- und CSV-Inventar, Gliederungs-Finale, 4 neue Figurvorschläge abb_5_1b / 5_2b / 5_7 / 5_5b).
- **Quellen** (für Interpretation):
  - ROA/ROE/EBIT-Marge → Dichev & Tang (2009) als φ₁-Benchmark (Earnings-Persistence). ✅
  - FCF-Marge → Dechow (1994): Accrual-Timing erklärt abweichende Dynamik. ✅
  - ROE×D/E σ-Kopplung (ρ = 0,82) → Christie (1982): Leverage-Effekt. ✅
  - Nissim & Penman (2001): DuPont-Mechanik ROE = ROA × (1+D/E). ✅
- **Kriterien „perfekt":**
  - Drei-Schichten-Hierarchie als Leitmotiv in **jedem** Unterabschnitt aufgreifen.
  - R²-Median und Signifikanzrate pro Kennzahl (6.521 Schätzungen) als Einordnungs-Tableau.
  - Sektor-Heatmap + Quadranten-Scatter als zentrale Abbildungen.
  - Robustheit (4 Modellvarianten, 4 Stichproben, Financial-Services-Sonderanalyse) als transformationsrobuste Fundierung.
  - Ökonomische Deutung am Ende jedes Unterabschnitts (marktgetrieben vs. managementgesteuert).

### Kap. 6 — FF2 Interdependenzen + Events (8–10 Seiten) · Stand: **Rohtext vorhanden, Cramér's-V-Restfragment**

- **Stand PDF (S. 80–93):** Überschriften 6.1 Methodik, 6.2.1–6.2.4 (Querschnitt), 6.3.1–6.3.3 (Events), 6.4 Zusammenfassung. **Problem:** S. 88 hat noch Abschnitt 6.2.4 „Quadrantenüberschneidungen (Cramér's V)" — muss raus oder umformuliert werden (Prof-Anweisung 26.03.).
- **Vorarbeit:**
  - `output/FF2_Interdependenz_Events.md` (13,6 KB) inkl. φ₁- und σ-Korrelationsmatrizen, Befunde 1–6, Event-Analyse mit 3 Peak-Windows (Dot-Com 2001Q4, GFC 2009Q2, COVID 2020Q3).
  - `output/FF2_Ergebnisse.docx` (605 KB mit Plots).
- **Quellen:**
  - Blockstruktur-Bestätigung → Sloan (1996), Fama & French (2000) — Earnings-Kohärenz.
  - ROE×D/E σ-Kopplung → Christie (1982) Leverage-Effekt.
  - EBIT×FCF σ-Kopplung (ρ=0,78), φ₁-Entkopplung (ρ=0,15) → Dechow (1994) Accrual-Timing.
  - Event-Analyse (Dot-Com, GFC, COVID) → Comin & Philippon (2006) Firm-Level-Volatility.
- **Kriterien „perfekt":**
  - Spearman **durchgängig**, nicht Cramér's V. Bonferroni α/42 oder Caveat.
  - Blockstruktur als direkter FF1-Anschluss (Hierarchie aus neuer Perspektive).
  - Event-Analyse als datengetriebene Alternative zu parametrischen Strukturbruchmodellen.
  - Quadrantenklassifikation als prädiktiv für Krisenreaktionen validieren.

### Kap. 7 — FF3 Externe Validierung (8–10 Seiten) · Stand: **Rohtext vorhanden**

- **Stand PDF (S. 94–116):** Struktur komplett. Substantiell: S. 108 (7.4.2 K-Means-Cluster-Methodik-Notiz), S. 114 (7.5.2 Financial-Services-Vergleich). Cramér's V bleibt hier als Effektstärkemaß für χ²-Tests.
- **Vorarbeit:**
  - `output/FF3_Externe_Validierung.md` (13,3 KB) mit Konsistenz-Scores, dominanten Quadranten, χ²-Tests, Größeneffekten (bis ρ=−0,53 mit σ), K-Means 2-Cluster-Lösung (81 %/19 %), Financial-Services-Vergleich.
  - `output/FF3_Ergebnisse.docx` (517 KB).
  - `output/external_validation/` (Plots).
- **Quellen:**
  - Größeneffekt → Fama & French (1992). ✅
  - Financial Services Sonderdynamik → Basel III / Solvency II-Argumente.
  - K-Means-Referenz → Dzuba & Krylov (2021). ✅
- **Kriterien „perfekt":**
  - χ²-Tests mit Cramér's V als Effektstärke. Bonferroni α/7 oder Caveat.
  - Drei Ebenen: Konsistenz-Problem → Sektor × Quadrant → Größe × Quadrant.
  - K-Means als datengetriebener Robustheitscheck.
  - Financial-Services-Sonderanalyse mit Tabelle φ₁-Mediane Hauptanalyse vs. Financial Services.

### Kap. 8 — Diskussion (6–8 Seiten) · Stand: **leer**

- **Stand PDF:** leeres Skelett.
- **Vorarbeit:** GLIEDERUNG_MASTERARBEIT.md.
- **Muss-Themen (aus 26.03.):**
  - **US-GAAP vs. IFRS**: Bewertungsspielräume, Management-Anreize, Implikation für Quartalskorrektur („natürlicher Geschäftsverlauf vs. Bilanzierung"). Literatur: Standard Accounting-Paper zu IFRS-vs-GAAP.
  - **Survivorship Bias**: was bleibt trotz Robustheit als Einschränkung? Technologie-Unternehmen während Dot-Com.
  - **Mehrfachtesten**: Bonferroni-Caveat offen ansprechen.
  - **Keine Kausalanalyse**: Mean-Reversion ≠ Kausalität. Klare Abgrenzung.
  - **Vergleich mit Dichev & Tang (2009)**: FCF-Marge-Dynamik als Bezug zur Accrual-Literatur.
  - **Elefanten & Wolken**: welche Befunde sind aus Hypothesen abgeleitet, welche explorativ?
- **Kriterien „perfekt":** Limitationen ehrlich, nicht übertrieben. Interpretationsbogen schließen.

### Kap. 9 — Fazit und Ausblick (2–3 Seiten) · Stand: **leer**

- **Stand PDF:** leeres Skelett.
- **Kriterien „perfekt":** Zusammenfassung der drei Schichten, wissenschaftlicher Beitrag (AR auf Differenzen als zweite Perspektive zur Earnings-Persistence-Literatur), Praxisbezug (Typologie für Investoren/Analysten), Ausblick (Europa-Daten, MC-Simulationen, Fama-French-Regression — nur als „weiterer Forschungsbedarf").

---

## 3. „Perfektes Kapitel" — Bewertungsraster (Stollhoff)

Aus Meeting 26.03. + Mail 14.03. abgeleitet. Anwendbar auf jedes Kapitel.

1. **Interpretation vor Beschreibung.** Jede Zahl mit ökonomischer Erklärung (WARUM).
2. **Quelleneinbettung.** Für jeden zentralen Befund: Wie sagt die Literatur es? Wo stimmt es überein, wo weicht es ab?
3. **Exploratives explizit.** Getrennt von hypothesengetriebenem Befund benennen.
4. **Nur Verstandenes.** Keine komplexen Methoden nennen, die nicht eigenständig beherrscht werden.
5. **Großer Bogen.** Jedes Kapitel schließt an den roten Faden an (siehe GLIEDERUNG_MASTERARBEIT.md: 5-Stufen-Logik).
6. **Mehrfachtesten-Caveat** durchgängig, wo > 1 Test gerechnet wird.
7. **Trennung Methodik ↔ Diskussion.** Neue methodische Limitationen gehören in Diskussion, nicht in Methodenbeschreibung.
8. **Verteidigbare Komplexität.** Stollhoff-Originalzitat: „Der Umfang reicht völlig aus. Sie müssen nicht noch mehr draufsetzen."

---

## 4. Quellenlandkarte (10 PDFs + 2 Lehrbücher)

| # | Quelle | Vorhanden | Hauptnutzen in Kapitel |
|---|---|:---:|---|
| 1 | Dechow (1994) Accruals & Cash Flows | ✅ | Kap. 5.2.4 (FCF), Kap. 6.2 (σ-Kopplung), Kap. 8 |
| 2 | Dzuba & Krylov (2021) K-Means Financial | ✅ | Kap. 4.3.4, Kap. 7.4 |
| 3 | Dichev & Tang (2009) Earnings Volatility | ✅ | **Hauptreferenz**: Kap. 2.2, 3.1, 4.2, 5.1, 8 |
| 4 | Love & Zicchino (2006) Panel VAR | ✅ | Kap. 4.2 (VAR-Gegenargument), Kap. 8 |
| 5 | Eljelly (2004) Liquidity-Profitability | ✅ | Kap. 3.3, 6.2 |
| 6 | Nissim & Penman (2001) Ratio Analysis | ✅ | Kap. 2.1, 3.1, 6.2 |
| 7 | Fama & French (1992) Cross-Section | ✅ | Kap. 3.2, 7.3 |
| 8 | Christie (1982) Stock Variances | ✅ | Kap. 6.2 (ROE×D/E) |
| 9 | Wave-Particle Duality (2024, PLOS ONE) | ✅ | Thematischer Verwandter, optional |
| 10 | Fairfield & Yohn (2001) Asset Turnover | ✅ | Kap. 2.2 (Diffs-Argument) |
| L1 | Hamilton (1994) Time Series | ✅ (phys.) | Kap. 2.2, 2.3, 4.2 |
| L2 | Wooldridge Introductory Econometrics | ✅ (phys.) | Kap. 2.3, 4.2 |
| — | **Sloan (1996)** Accruals vs. Cash Flows | ❌ zu beschaffen | Kap. 3.1, 8 |
| — | **Fama & French (2000)** Forecasting Profitability | ❌ zu beschaffen | Kap. 3.1 |
| — | **Comin & Philippon (2006)** Firm Volatility | ❌ zu beschaffen | Kap. 3.2, 6.3 |
| — | **Penman** Financial Statement Analysis | ❌ zu prüfen | Kap. 2.1 Kennzahl-Definitionen |
| — | „Ep"-Quelle (NotebookLM) | ❌ ungeklärt | — |

**Aktion diese Woche:** Sloan, Fama-French 2000, Comin-Philippon, Penman beschaffen (Uni-Zugang oder Sci-Hub).

---

## 5. Gaps & Prioritäten

### P1 — Blockierer für Abgabe (diese Woche)

- [ ] **Kap. 4 Restpunkte** (7 Items, siehe §2 Kap. 4) — Methodik sauber schließen.
- [ ] **Cramér's V FF2-Abschnitt (6.2.4)** im PDF/PPTX entfernen bzw. umformulieren auf Spearman.
- [ ] **Notebook 02.3/02.4 & METHODIK_DISKUSSION.md**: Cramér-V-Reste entfernen, Monte-Carlo-Reste entfernen.
- [ ] **Literatur beschaffen**: Sloan, Fama-French 2000, Comin-Philippon, Penman.

### P2 — Kernschreibphase (21.04.–04.05.)

- [ ] **Kap. 2 Theorie** (4–5 Tage) — Hamilton/Wooldridge/Pesaran-Smith einarbeiten.
- [ ] **Kap. 3 Forschungsstand** (3–4 Tage) — Literatureinordnung entlang 3.1–3.5.
- [ ] **Kap. 5 FF1 konsolidieren** (4–5 Tage) — Rohtext + Grafiken + Interpretation zusammenführen. FF1_UEBERSICHT.md als Navigations-Karte nutzen; 4 vorgeschlagene neue Figuren (abb_5_1b, 5_2b, 5_7, 5_5b) prüfen.
- [ ] **Kap. 6 FF2 konsolidieren** (3–4 Tage) — Spearman-Narrativ, Event-Analyse.
- [ ] **Kap. 7 FF3 konsolidieren** (3–4 Tage) — Konsistenz-Scores, χ², Größe, K-Means, FinServ.

### P3 — Einordnung & Abschluss (05.05.–14.05.)

- [ ] **Kap. 8 Diskussion** (4–5 Tage) — IFRS/USGAAP, Survivorship, Multiple Testing, Kausalität, Elefanten/Wolken.
- [ ] **Kap. 9 Fazit** (1–2 Tage).
- [ ] **Kap. 1 Einleitung** (1–2 Tage) — zum Schluss.

### P4 — Feinschliff (15.05.–18.05.)

- [ ] Querverweise prüfen (Kapitel-X → echte Nummern).
- [ ] Grafiken-Druckqualität, Titelblatt, Verzeichnisse (Abbildung, Tabelle, Literatur, Abkürzungen).
- [ ] Korrekturlesen.

### Puffer 19.05.–21.05. · Abgabe 21.05.

### P5 — nach Abgabe (Verteidigung + Artikel)

- Europa-Daten-Analyse (wieder aktivierbar, für Bonusfolie).
- Monte-Carlo-Simulationen (saubere Implementierung).
- Fama-French-Regression (Quadrant auf Size/Value/Momentum).
- Artikel mit Stollhoff (Angebot vom 26.03.).

---

## 6. Arbeits-Konventionen

- **Master-Dokument** für Schreibstand: `Text/Text.pptx`. Letzter PDF-Export in `mnt/uploads/` (139 Seiten).
- **Arbeitsdateien**: `Text/` (Planung, Übersichten, dieses Dokument).
- **AI-Rohdraft**: `Finale_Kapitel/` (Kapitel_5_FF1_Ergebnisse.md als Textbasis, nicht final — Feedback in `ERWEITERUNGSPOTENZIALE.md`).
- **Ergebnis-Quellen**: `output/` (CSVs, FF-MDs, Plots, Dashboard).
- **Prof-Kommunikation**: `Prof/` (Mails, Meeting-Transkripte, Feedback-Dokumente).
- **Living Briefings**:
  - `COWORK_KONTEXT.md` — Session-Briefing, Konventionen, Methodik-Fixpunkte.
  - `Text/FF1_UEBERSICHT.md` — FF1-spezifische Navigation (Grafiken, CSVs, Gliederung, Gaps).
  - `Text/MASTER_REFERENZ.md` — dieses Dokument (ganzheitliche Übersicht).
  - `Text/GESAMTPLAN_APRIL_2026.md` + `Text/PROJECT_STATUS.md` — Zeitplan & Rollen.
  - `Text/GLIEDERUNG_MASTERARBEIT.md` — detaillierter Schreibplan pro Kapitel.

---

## 7. Kernzahlen zum Merken

- **Datenbasis:** 932 Unternehmen · 100 Quartale · 7 Kennzahlen · 6.521 Regressionen.
- **Drei-Schichten-Hierarchie (φ₁-Median):** ROA/ROE/EBIT −0,43 · FCF −0,46 · CR −0,17 · D/E −0,09 · EK-Quote −0,04.
- **Levels-Persistenz (φ₁):** Kapitalstruktur 0,87–0,93 · Profitabilität 0,10–0,57.
- **Signifikanzraten:** Profitabilität 90–97 % · Liquidität 46 % · Kapitalstruktur ≪.
- **Halbwertszeit ROA:** ≈ 0,33 Quartale ≈ 1 Monat.
- **Spearman ρ (φ₁ × σ):** < 0,19 bei Profitabilität (Trennbarkeit bestätigt).
- **Blockstruktur (φ₁-Korrelation innerhalb Profitabilität):** ROA × ROE = 0,78.
- **Leverage-σ-Kopplung:** ROE × D/E = 0,82 (Christie 1982).
- **Dominante Quadranten-Verteilung:** Persistent-Stabil 30 % · Korrektiv-Volatil 27 % · Korrektiv-Stabil 22 % · Persistent-Volatil 21 %.
- **Größeneffekt:** bis ρ = −0,53 Mitarbeiter × σ — Größe dämpft Volatilität, nicht Mean-Reversion.
