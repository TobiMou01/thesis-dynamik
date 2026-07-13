# Prompt: Kapitel 4 (Methodik) überarbeiten

## Kontext

Ich schreibe meine Masterarbeit "Zeitreihenbasierte Analyse der Dynamik von Finanzkennzahlen börsennotierter Unternehmen" (TH Wildau, Abgabe 21. Mai 2026, Betreuer: Prof. Stollhoff + Prof. Steglich). Sprache: akademisches Deutsch.

Methodik: AR(1) auf ersten Differenzen — ΔY(t) = c + φ₁·ΔY(t−1) + ε(t) — für 7 Finanzkennzahlen (ROA, ROE, EBIT-Marge, FCF-Marge, Current Ratio, Debt/Equity, EK-Quote), 932 US-Unternehmen (S&P 1500), 100 Quartale Q1/2000–Q4/2024. φ₁ = Korrekturgeschwindigkeit, σ(ΔY) = Volatilität. Individuelle OLS-Regression pro Unternehmen-Kennzahl-Kombination (6.521 Regressionen). Quadrantenklassifikation via Median-Split auf φ₁ × σ.

Wichtige Regeln vom Betreuer (Prof. Stollhoff):
- AR(1) ist ex ante festgelegt — kein Modellwechsel nach Datensicht
- Monte-Carlo komplett entfernt
- Cramér's V ersetzt durch Spearman-Rangkorrelation (außer FF3 Sektor, dort χ² + Cramér's V korrekt)
- Hypothesengeleitet vs. explorativ klar trennen
- Kein weiterer Scope-Ausbau

Ich lade die Datei `Kapitel_4_Methodik.docx` hoch. Das ist mein Arbeitsdokument, in dem ich jetzt direkt überarbeiten will. Bitte NICHT den Text für mich umschreiben — ich schreibe selbst. Du bist mein Sparringspartner und gibst mir Anweisungen, was ich wo ändern soll.

---

## Aufgabe: Kapitel 4 strukturell überarbeiten

Mein Kapitel 4 hat drei diagnostizierte Probleme:

### Problem 1: Doppelungen mit Kapitel 2 (Theoretische Grundlagen)

Folgende Inhalte stehen SOWOHL in Kapitel 2 ALS AUCH in Kapitel 4 — sie müssen in Kap. 4 durch Verweise ersetzt werden:

| Was | Wo in Kap. 4 | Wo in Kap. 2 | Aktion |
|-----|-------------|-------------|--------|
| AR(1)-Modellgleichung + Interpretation φ₁ und σ | 4.2 Schritt 2 | 2.3 | In 4.2 nur Verweis: "Das in Abschnitt 2.3 eingeführte AR(1)-Modell wird geschätzt." |
| Drei Vorteile erster Differenzen + Fairfield & Yohn | 4.2 Schritt 1 | 2.2 | In 4.2 nur Verweis auf 2.2 |
| Quadranten-Labels-Tabelle + Beschreibungen | 4.3 Konstruktion | 2.4 | In 4.3 nur Verweis: "Die in Abschnitt 2.4 eingeführte Klassifikation wird per Median-Split operationalisiert." |
| MacCallum-Kritik + Rucker-Relativierung + Fama-French-Analogie | 4.3 Median-Split | 2.4 | Komplett raus aus 4.3, steht schon in 2.4 |
| Warum nicht VAR/GARCH | 4.4 Modellwahl | 2.3 | Raus aus 4.4, steht schon in 2.3 |
| Uniformitäts-Trade-off | 4.4 | 2.2 | Raus aus 4.4, steht schon in 2.2 |
| Vier Modellvarianten (Tabelle + Beschreibung) | 4.4 Alternative AR | 2.3 | Tabelle raus, nur Verweis auf 2.3 |

WICHTIG: Nichts davon darf verloren gehen! Wenn etwas in Kap. 4 ausführlicher steht als in Kap. 2, muss ich den besseren Teil ERST in Kap. 2 einbauen, BEVOR ich ihn aus Kap. 4 entferne. Hilf mir, das Stück für Stück durchzugehen.

### Problem 2: Ergebnisse in der Methodik

Folgende Inhalte sind ERGEBNISSE und gehören nach Kapitel 5 (oder 7):

| Was | Wo in Kap. 4 | Wohin verschieben |
|-----|-------------|------------------|
| φ₁-Mediane-Tabelle (alle 4 Spezifikationen) + Interpretation | 4.4 "Alternative AR-Spezifikationen" | → Kap. 5 Robustheit |
| Modellvergleichs-Plot (image3.jpeg) | 4.4 | → Kap. 5 Robustheit |
| Spearman-Korrelationstabelle (φ₁ vs. σ) mit konkreten Zahlen | 4.3 Validierung | → Kap. 5 oder 7 |
| Quadranten-Scatterplot (image2.png) | 4.3 | → Kap. 5 (oder Kap. 2 als konzeptuelle Illustration) |
| Konkreter Absatz über Survivorship-Bias-Ergebnisse (φ₁-Mediane bleiben stabil) | 4.1 | → Kap. 5 Robustheit |

In Kap. 4 bleibt jeweils nur das DESIGN stehen: "Dies wird durch X geprüft (Ergebnisse in Abschnitt Y)."

### Problem 3: Fehlende Inhalte (für später, NICHT jetzt)

Diese Punkte müssen noch ergänzt werden, aber NACH dem Aufräumen:
- Residuendiagnostik: Ljung-Box, Durbin-Watson — werden die Residuen geprüft? (→ in 4.2 ergänzen)
- Drift-Konstante c: Wird geschätzt, aber nie diskutiert (→ in 4.2 ergänzen)
- T = 98 klären (nicht 99): 100 − 1 Differenz − 1 Lag = 98
- 6.521 statt 6.524: Drei Kennzahlen konnten nicht geschätzt werden, das dokumentieren
- Konfirmatorisch vs. explorativ: Fehlt in der docx, steht nur in der Markdown-Version
- Abschnitt 4.5: Tests begründen mit Wooldridge/Hamilton statt nur auflisten
- Alle "Kapitel X" Platzhalter durch echte Verweise ersetzen
- TODO zu Prof. Steglich (USGAAP vs. IFRS) klären oder entfernen

---

## Drei Bücher, die ich einarbeiten will

- **Hamilton** (Time Series Analysis, 1994): AR-Prozess-Eigenschaften, Stationarität, warum OLS bei Zeitreihen funktioniert → gehört in Kap. 2 (Theorie) und Kap. 4 (OLS-Begründung)
- **Wooldridge** (Econometrics): OLS-Annahmen, HAC-Standardfehler (Newey-West), Pooled-OLS-Bias → gehört in Kap. 4 (Schritt 3, Testverfahren)
- **Penman** (Financial Statement Analysis): Transiente vs. permanente Earnings-Komponenten, ökonomische Logik der Kennzahlen-Dynamik → gehört in Kap. 2 (ökonomische Begründung der Drei-Schichten)

---

## Arbeitsweise

1. Gehe mit mir Abschnitt für Abschnitt durch Kapitel 4
2. Für jeden Abschnitt: Sage mir was raus muss, was bleiben darf, was fehlt
3. Wenn etwas raus muss: Sage mir wohin ich es kopieren soll (Kap. 2, 5, oder 7), BEVOR ich es lösche
4. Schreibe mir KEINE fertigen Textblöcke — sage mir stattdessen in 1-2 Sätzen was der Absatz aussagen soll, und ich formuliere ihn selbst
5. Wenn ich einen Absatz geschrieben habe, gib mir inhaltliches Feedback (stimmt die Aussage? fehlt was? ist es zu vage?)

Lass uns mit Abschnitt 4.1 (Datengrundlage) anfangen.
