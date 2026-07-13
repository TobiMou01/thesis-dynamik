# Gesamtplan Masterarbeit — Stand 03. April 2026

**Abgabe:** 21. Mai 2026 (7 Wochen)
**Titel:** Zeitreihenbasierte Analyse der Dynamik von Finanzkennzahlen

---

## Was ist erledigt?

### Analyse & Code
- AR(1)-Pipeline komplett (diff1, levels, AR(2), diff4)
- FF1–FF3 Ergebnisse in CSVs
- Dashboard v4 (8 Tabs, 31 MB)
- Alle Plots generiert

### Stollhoff-Meeting 26.03 — bereits umgesetzt
- Monte-Carlo-Benchmark aus Kapitel 4 entfernt (Text + Tabelle)
- Cramér's V als Hauptmethode für FF2 entfernt → Spearman bleibt
- Cramér's V bleibt in FF3 als Effektstärkemaß für χ²-Tests (korrekt)
- Hinweis auf multiples Testen in 4.5 ergänzt
- Tabelle 4.3 auf 3 Spalten reduziert (Kennzahl, Spearman ρ, Signifikanz)

### Dokumente
- Kapitel 4 Methodik: geschrieben und überarbeitet
- Arbeitsdokument: 4 Einfügungen mit Prof-Feedback (blau markiert)
- GLIEDERUNG_MASTERARBEIT.md: vollständiger Schreibplan für alle Kapitel

---

## Stollhoff-Meeting 26.03 — Entscheidungen (Referenz)

| Entscheidung | Status |
|---|---|
| Monte-Carlo-Benchmark RAUS | ✅ Umgesetzt in Kap. 4 |
| Cramér's V RAUS für FF2 → Spearman | ✅ Umgesetzt in Kap. 4.5 |
| Cramér's V BLEIBT für FF3 (χ²-Effektstärke) | ✅ Korrekt in Kap. 4.5 |
| Keine neuen Kennzahlen | ✅ Entschieden — FCF-Marge ↔ Dichev & Tang vergleichen |
| Keine Europadaten (nur Verteidigung) | ✅ Geparkt |
| Multiples Testen: Bonferroni oder Caveat | ⏳ Hinweis in 4.5, muss in Ergebniskapiteln durchgezogen werden |
| USGAAP vs. IFRS → Diskussionskapitel | ⏳ Kapitel 8 |
| Interpretation = Hauptbewertungskriterium | ⏳ Durchgehend beim Schreiben beachten |
| Quelleneinbettung überall | ⏳ Durchgehend beim Schreiben |
| "Wolken und Elefanten" — exploratives klar kennzeichnen | ⏳ Durchgehend |
| Nichts schreiben was du nicht verstehst | ⏳ Durchgehend |

---

## PHASE 1: Methodik finalisieren (diese Woche, bis ~6. April)

### 1.1 Kapitel 4 — Restpunkte fixen
- [ ] **10 Issues aus Review v2** — TODO-Notes, Grammatik, T=98/99-Korrektur
- [ ] **Kapitel-X-Platzhalter** drin lassen (Gliederung ändert sich noch)
- [ ] **Selbstreferenz in 4.4** fixen: "werden in Abschnitt 4.4 detailliert dargestellt" ist zirkulär
- [ ] **Quadrantenlinie in Abb. 4.1** fehlt (eigene Notiz: "2. Quadrantenlinie fehlt!!!")
- [ ] **Rote Tabellenfarbe (EE0000)** in Tabelle 4.3 auf Schwarz ändern
- [ ] **Lehrbuch-Referenzen einfügen:** Hamilton bei Stationarität (4.2 Schritt 1), Wooldridge bei AR-Herleitung (4.2 Schritt 2) — Bücher sind vorhanden
- [ ] **Monte-Carlo in 4.3/2.4** — Abschnitt zur mechanischen Abhängigkeit φ₁×σ: MC-Benchmark-Verweis entfernen oder umformulieren (nur Spearman-Korrelation |ρ| < 0,19 als Argument)
- [ ] **Bonferroni** konkreter spezifizieren: α/42 für FF2-Korrelationen (21 Paare × 2 Matrizen), α/7 für FF3 χ²-Tests

### 1.2 Code-Bereinigung (optional, niedrige Priorität)
- [ ] Prüfen ob alle 4 Modellvarianten sauber in ar_features_all.csv sind
- [ ] Datenquelle benennen (SimFin? Compustat? Bloomberg?) — für Kap. 4.1
- [ ] Outlier-Behandlung/Winsorizing aus Code dokumentieren — für Kap. 4.1

---

## PHASE 2: Literatur beschaffen (parallel zu Phase 1, bis ~8. April)

### Noch zu beschaffen (Artikel — online/Uni-Zugang)
- [ ] **Sloan (1996)** — "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?" → unverzichtbar für Kap. 3.1
- [ ] **Fama & French (2000)** — "Forecasting Profitability and Earnings" → Mean-Reversion von Profitabilität, Kap. 3.1
- [ ] **Comin & Philippon (2006)** — "The Rise in Firm-Level Volatility" → Diversifikationshypothese, Kap. 3.2

### Bereits vorhanden
- Hamilton (1994) — Lehrbuch ✅ (physisch)
- Wooldridge — Lehrbuch ✅ (physisch)
- Penman — Lehrbuch (für Kennzahl-Definitionen) → noch prüfen ob vorhanden
- 10 PDFs aus Quellenliste ✅

### Recherche-Aufgaben
- [ ] "Ep"-Quelle aus NotebookLM identifizieren
- [ ] 1–2 Arbeiten zu regulatorischen Effekten auf Bilanzkennzahlen (Basel III)
- [ ] Literatur zu Median-Split in Finanzforschung (oder Fama-French Portfolio-Sorts als Referenz)
- [ ] Arbeit zu AR-Parametern als Clustering-Features (direkter Vorläufer?)

---

## PHASE 3: Kapitel schreiben (Kernphase, ~7. April bis ~10. Mai)

### Empfohlene Reihenfolge

**Woche 1–2 (7.–20. April): Theorie + Forschungsstand**

| Prio | Kapitel | Seiten | Kernaufgabe | Vorbedingung |
|---|---|---|---|---|
| 1 | Kap. 2.2 + 2.3 | 4 | Mean-Reversion-Theorie, AR-Modelle formal | Hamilton/Wooldridge ✅ |
| 2 | Kap. 2.1 | 2 | 7 Kennzahlen, Drei-Kategorien-Logik | Penman-Lehrbuch |
| 3 | Kap. 2.4 | 1,5 | Quadrantenklassifikation theoretisch | — |
| 4 | Kap. 3.1–3.4 | 5–6 | Literatureinordnung + Lücke | Sloan, Fama & French 2000 |
| 5 | Kap. 3.5 | 1 | Forschungslücke + Beitrag | Kap. 3.1–3.4 fertig |

**Woche 3–4 (21. April – 4. Mai): Ergebnisse FF1–FF3**

| Prio | Kapitel | Seiten | Kernaufgabe | Vorbedingung |
|---|---|---|---|---|
| 1 | Kap. 5 (FF1) | 12–15 | Drei-Schichten-Hierarchie + Interpretation | Kap. 2+3 als Referenz |
| 2 | Kap. 6 (FF2) | 8–10 | Interdependenzen + Events + Interpretation | Kap. 5 fertig |
| 3 | Kap. 7 (FF3) | 8–10 | Externe Validierung + Interpretation | Kap. 6 fertig |

Hinweis: FF-spezifische Methodik-Einschübe (je ~1 Seite) kommen an den Anfang von Kap. 5, 6, 7 (hybrider Ansatz aus GLIEDERUNG).

**Woche 5 (5.–11. Mai): Diskussion + Fazit**

| Prio | Kapitel | Seiten | Kernaufgabe |
|---|---|---|---|
| 1 | Kap. 8 | 6–8 | Interpretation, Literatureinordnung, Limitationen, USGAAP/IFRS |
| 2 | Kap. 9 | 2–3 | Zusammenfassung, Beitrag, Ausblick |

**Woche 6 (12.–18. Mai): Einleitung + Feinschliff**

| Prio | Kapitel | Seiten | Kernaufgabe |
|---|---|---|---|
| 1 | Kap. 1 | 2–3 | Einleitung (zum Schluss, wenn alles steht) |
| 2 | Alle | — | Querverweise, Kapitel-X → echte Nummern, Roter Faden prüfen |
| 3 | Alle | — | Grafiken-Integration, Formatierung, Titelblatt, Verzeichnisse |

**Woche 7 (19.–21. Mai): Puffer + Abgabe**
- Korrekturlesen
- Letzte Formatierung
- Druck / Abgabe

---

## PHASE 4: Durchgehende Qualitätskriterien

Diese Punkte gelten für JEDES Kapitel:

### Interpretation (Stollhoff: "Hauptbewertungskriterium")
- Jede Zahl braucht eine ökonomische Erklärung (WARUM, nicht nur WAS)
- Geschäftsmodell-Bezüge bei Sektorergebnissen
- Nicht nur beschreiben, sondern einordnen

### Quelleneinbettung
- Jeder wichtige Befund braucht einen Literaturvergleich
- Dichev & Tang (2009) = Hauptreferenz in Kap. 2, 3, 4, 5
- Nissim & Penman (2001) = DuPont in Kap. 2, 3, 6
- Fama & French (1992) = Größeneffekt in Kap. 3, 7
- Hamilton/Wooldridge = AR-Theorie in Kap. 2, 4

### Explorativ vs. Konfirmatorisch
- Hypothesen aus FF1–FF3 = konfirmatorisch
- Alles was "überraschend" ist = klar als explorativ kennzeichnen
- Keine Post-hoc-Rationalisierungen

### Multiples Testen
- FF2: 21 Kennzahlenpaare × 2 Korrelationsmatrizen → Bonferroni α/42 oder Caveat
- FF3: 7 χ²-Tests → Bonferroni α/7 oder Caveat
- Event-Analyse: Bonferroni bei Mann-Whitney U-Tests

---

## Offene Fragen (noch zu klären)

| Frage | Wann klären? | Mit wem? |
|---|---|---|
| Steglich-Feedback zu USGAAP/IFRS | Wenn Steglich wieder da ist | Prof. Steglich |
| Datenquelle exakt benennen | Beim Schreiben von Kap. 4.1 | Eigene Recherche im Code |
| Penman-Lehrbuch vorhanden? | Sofort | Eigene Bibliothek |
| "Ep"-Quelle identifizieren | Diese Woche | NotebookLM |
| Granger-Kausalität: ja/nein? | Entschieden: NEIN (niedrige cross-kategoriale ρ als Argument) | — |
| Fama-French-Regression (Size/Value auf Quadranten): ja/nein? | Entschieden: NEIN (Scope) | — |

---

## Zusammenfassung: Die nächsten 7 Wochen

```
Woche  Kalender        Fokus
─────  ──────────────  ──────────────────────────────────
  1    03.–06. Apr     Kap. 4 Restpunkte + Literatur beschaffen
  2    07.–13. Apr     Kap. 2 (Theorie) schreiben
  3    14.–20. Apr     Kap. 3 (Forschungsstand) schreiben
  4    21.–27. Apr     Kap. 5 (FF1) schreiben
  5    28. Apr–04. Mai Kap. 6 (FF2) + Kap. 7 (FF3) schreiben
  6    05.–11. Mai     Kap. 8 (Diskussion) + Kap. 9 (Fazit)
  7    12.–18. Mai     Kap. 1 (Einleitung) + Feinschliff + Querverweise
  --   19.–21. Mai     PUFFER + ABGABE
```

**Wichtigste Regel (Stollhoff):** Nichts Neues hinzufügen. Keine neuen Methoden, keine neuen Daten. NUR schreiben, interpretieren, einordnen.
