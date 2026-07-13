# E-Mail-Draft – Vorab-Mail für Termin 26.03.2026

**An:** Prof. Stollhoff, Prof. Steglich
**Betreff:** Zwischenstand & Gesprächsgrundlage für Donnerstag (26.3.)

---

Sehr geehrter Herr Prof. Stollhoff, sehr geehrter Herr Prof. Steglich,

vielen Dank für Ihre Rückmeldung und die hilfreiche Einordnung der AR-Modellvarianten. Als Vorbereitung auf unser Gespräch am Donnerstag möchte ich Ihnen zeigen, wie sich die Ergebnisse seit meiner letzten Mail entwickelt haben — insbesondere, wie ich FF1 konkret aufbauen werde, und wo ich bei FF2 und FF3 stehe.

---

## FF1: Dynamik-Unterschiede — Aufbau und Ergebnisse

### Kernbefund: Drei-Schichten-Hierarchie

Die AR(1)-Analyse auf ersten Differenzen bestätigt die in meiner letzten Mail skizzierte Hierarchie über alle 932 Unternehmen hinweg. In der beigefügten Grafik [Profil-Scatter + Boxplots] ist das Muster gut sichtbar:

- **Profitabilitätskennzahlen** (ROA, ROE, EBIT-Marge, FCF-Marge): eng geclustert bei φ₁ ≈ −0,43 bis −0,46, Signifikanzrate 90–97%. Quartalsveränderungen korrigieren sich im Folgequartal systematisch zu 43–46%.
- **Liquidität** (Current Ratio): φ₁ ≈ −0,17, nur 46% signifikant. Schwache, inkonsistente Mean-Reversion.
- **Kapitalstruktur** (D/E, EK-Quote): φ₁ ≈ −0,04 bis −0,09. De facto kein AR-Signal auf Differenzen. Auf Niveaus zeigen genau diese Kennzahlen die höchste Persistenz (φ₁ = 0,87–0,93) — das ist konsistent.

Die Drei-Schichten-Hierarchie ist die zentrale Aussage von FF1 und lässt sich ökonomisch durch die Unterscheidung marktgetriebener (Profitabilität) vs. managementgesteuerter (Bilanzstruktur) Kennzahlen erklären.

### Quadrantenklassifikation

Neben der Hierarchie differenziere ich innerhalb jeder Schicht über ein Quadrantenframework aus φ₁ (Mean-Reversion-Stärke) und σ(ΔY) (Änderungsvolatilität). Die beigefügte Grafik [ROA-Scatter] zeigt das am Beispiel ROA: vier klar unterscheidbare Dynamik-Typen (Korrektiv-Stabil, Korrektiv-Volatil, Persistent-Stabil, Persistent-Volatil), die durch K-Means als Robustheitscheck bestätigt werden.

### Einordnung anhand der Literatur

Ich habe die Ergebnisse gegen mehrere literaturbasierte Thesen geprüft. Ein paar zentrale Befunde:

**Profitabilität vs. Bilanzstruktur (Earnings-Persistence-Literatur):** Die Literatur berichtet niedrigere Persistenz bei Profitabilitätskennzahlen als bei Bilanzkennzahlen. Meine Daten bestätigen das auf beiden Ebenen — auf Niveaus (φ₁ = 0,10–0,36 vs. 0,80–0,93) und auf Differenzen (φ₁ = −0,43 bis −0,46 vs. −0,04 bis −0,09).

**Sektorale Volatilitätsunterschiede (Branchenliteratur):** Technology-Unternehmen zeigen wie erwartet höhere Änderungsvolatilität als Consumer Defensive (z.B. ROA σ: 0,019 vs. 0,015; Current Ratio σ: 0,403 vs. 0,215). Allerdings mit Nuancen: Utilities haben bei der EBIT-Marge höhere Volatilität als Technology (0,158 vs. 0,108), was durch Wetter-/Saisoneffekte erklärbar ist.

**Größeneffekt (Fama & French):** Größere Unternehmen (gemessen an Mitarbeiterzahl) zeigen stabilere Profile — Korrelationen bis ρ = −0,53 mit σ(ΔY). Entscheidend: Der Effekt gilt nur für die Volatilitätsdimension. Die Mean-Reversion-Stärke φ₁ ist größenunabhängig. Die beiden Achsen meines Quadrantenframeworks haben also unterschiedliche externe Treiber.

**Blockstruktur der Dynamik:** Die φ₁-Korrelationen innerhalb der Profitabilitätsschicht sind hoch (ROA×ROE ρ = 0,78), während schichtübergreifende Korrelationen unter 0,10 liegen. Profitabilitätskennzahlen bewegen sich also als Block — auch das deckt sich mit der Literatur zur Earnings-Kohärenz.

**Volatilität × Persistenz (Dichev & Tang 2009):** Der erwartete negative Zusammenhang existiert, ist aber schwächer als in der Literatur (Spearman ρ = −0,09 bis −0,24). Vermutlich, weil ich auf Differenzen arbeite und nicht auf Niveaus. Ob und wie ich das in der Arbeit einordne, würde ich gerne am Donnerstag besprechen.

### Modellwahl — Antwort auf Ihre Rückmeldung

Sie hatten in Ihrer letzten Mail angemerkt, dass die Wahl von Daten und Modellen zur Forschungsfrage passen und begründet werden sollte. Dazu habe ich Folgendes umgesetzt: Ich habe die Drei-Schichten-Hierarchie über vier AR-Spezifikationen getestet — AR(1) auf Differenzen, AR(1) auf Niveaus, AR(2) auf Differenzen und saisonale Differenzen (Δ₄Y). Die Rangordnung bleibt in allen Varianten stabil. Auf Niveaus kehrt sich das Vorzeichen erwartungsgemäß um (hohe Persistenz bei Bilanzstruktur, moderate bei Profitabilität), AR(2) verschärft die Befunde, und saisonale Differenzen zeigen konsistente Muster. Die Kernaussage ist also modellunabhängig — was ich als zentrales Robustheitsargument in der Arbeit verwenden werde.

Die Entscheidung für AR(1) auf ersten Differenzen als Hauptmodell begründe ich damit, dass es die Quartals-zu-Quartals-Dynamik am direktesten misst und die Mean-Reversion der Veränderungen — der zentrale Mechanismus — am interpretierbarsten abbildet. Die anderen Spezifikationen dienen als Robustheitschecks.

---

## FF2: Interdependenzen — Stand und Umsetzung

Die querschnittliche Analyse ist abgeschlossen: Spearman-Korrelationen und Cramér's V bestätigen die Blockstruktur aus FF1 — schichtinterne Kohärenz bei Profitabilität, Unabhängigkeit zwischen den Schichten. Zusätzlich zeigt sich eine ROE×D/E-Volatilitätskopplung (σ-Korrelation ρ = 0,82) als mechanischer Leverage-Effekt.

Für die zeitliche Dimension habe ich eine datengetriebene Event-Analyse umgesetzt: Drei Peak-Windows (Dot-Com 2001Q4, GFC 2009Q2, COVID 2020Q3) wurden rein aus den Daten identifiziert. Die Quadrantenklassifikation zeigt hier prädiktive Kraft — KORREKTIV-klassifizierte Unternehmen reagieren stärker, korrigieren aber schneller.

Granger-Kausalitätstests waren ursprünglich geplant, aber die niedrigen cross-kategorialen φ₁-Korrelationen (< 0,10) deuten darauf hin, dass dynamische Kausalität zwischen den Schichten gering ist. Ob ich diese Tests trotzdem durchführe oder die Querschnittsanalyse als ausreichend betrachte, würde ich gerne mit Ihnen besprechen.

---

## FF3: Externe Validierung — Stand und Umsetzung

Die Validierung der Quadrantenklassifikation gegen externe Strukturmerkmale ist weitgehend abgeschlossen:

- **Sektor × Quadrant:** Alle χ²-Tests hochsignifikant (p < 0,001), Cramér's V = 0,18–0,29. Branche beeinflusst die Zuordnung, erklärt sie aber nicht vollständig.
- **Größeneffekte:** Mitarbeiterzahl korreliert mit σ (bis ρ = −0,53), nicht mit φ₁. Die zwei Dimensionen haben unterschiedliche Treiber.
- **K-Means:** Zwei-Cluster-Lösung (81% stabile Mehrheit, 19% hochvolatile Minderheit) bestätigt, dass die Hauptdifferenzierung über die Volatilitätsachse läuft.
- **Financial Services:** Als Robustheitscheck zeigt der Finanzsektor identische Profitabilitäts-Mean-Reversion, aber deutlich stärkere bei Liquidität und Kapitalstruktur — erklärbar durch Basel III / Solvency II. Die Exklusion in der Hauptanalyse ist damit begründet.

Offen ist, ob eine Fama-French-Regression (Quadrantenzugehörigkeit auf Size/Value/Momentum-Faktoren) als zusätzlicher Validierungsschritt sinnvoll wäre, oder ob das den Scope der Arbeit sprengt.

---

## Termin und Organisatorisches

Den Termin am Donnerstag, 26.3., kann ich gerne wahrnehmen. Herr Prof. Steglich — könnten Sie mir noch eine kurze Rückmeldung geben, ob der Termin auch für Sie passt? Ich würde die Grafiken und ggf. weitere Ergebnisse bis dahin finalisieren, damit wir eine gute Gesprächsgrundlage haben.

Aktualisierter Zeitplan (Änderungen kursiv):
- W9/10 (aktuell): FF1-Ergebnisse finalisieren, Thesen-Einordnung, *Modellvergleich als Robustheit*
- W11/12: FF2 abschließen, FF3 erweitern
- W13/14: Verschriftlichung Einleitung, Theorie, Methodik
- W15–17: Verschriftlichung Ergebnisse, Diskussion
- W18: Revision, Formatierung
- Abgabe: 21. Mai

Mit freundlichen Grüßen
Tobias Mourier
