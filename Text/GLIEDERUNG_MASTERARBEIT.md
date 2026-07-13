# Gliederung & Schreibplan — Masterarbeit Tobias Mourier

**Titel:** Zeitreihenbasierte Analyse der Dynamik von Finanzkennzahlen
**Hochschule:** TH Wildau | Betreuer: Prof. Stollhoff, Prof. Steglich
**Abgabe:** 21. Mai 2026
**Stand:** 19. März 2026

---

## Roter Faden der gesamten Arbeit

Die Arbeit folgt einer aufbauenden Logik in fünf Stufen:

1. **Das Phänomen definieren** (Kap. 1–3): Was sind Finanzkennzahlen-Dynamiken, warum sind sie relevant, und was weiß die Literatur bereits?
2. **Das Werkzeug begründen** (Kap. 4): Warum misst AR(1) auf ersten Differenzen genau das, was die Forschungsfragen verlangen — und nicht etwas anderes?
3. **Das Muster zeigen** (Kap. 5 / FF1): Es gibt eine Drei-Schichten-Hierarchie. Sie ist robust.
4. **Das Muster verstehen** (Kap. 6 / FF2 + Kap. 7 / FF3): Die Schichten hängen intern zusammen, reagieren unterschiedlich auf Krisen, und werden durch externe Merkmale (Branche, Größe) mitbestimmt.
5. **Das Muster einordnen** (Kap. 8–9): Was bedeutet das für Theorie und Praxis, wo sind die Grenzen?

Jede Stufe baut auf der vorherigen auf. Der Leser sollte an keiner Stelle denken: "Warum erzählt er mir das jetzt?"

---

## Kapitelübersicht

| Kap. | Titel | Seiten (ca.) | Status |
|------|-------|:---:|--------|
| 1 | Einleitung | 2–3 | Noch nicht geschrieben |
| 2 | Theoretische Grundlagen | 8–10 | Noch nicht geschrieben |
| 3 | Stand der Forschung | 6–8 | Literatur gesammelt, Text fehlt |
| 4 | Methodik | 10–12 | Teilweise vorhanden (METHODIK_DISKUSSION.md) |
| 5 | FF1: Systematische Dynamikmuster | 12–15 | Ergebnisse fertig, Text teilweise |
| 6 | FF2: Interdependenzen und zeitliche Manifestation | 8–10 | Ergebnisse fertig, Text teilweise |
| 7 | FF3: Externe Validierung | 8–10 | Ergebnisse fertig, Text teilweise |
| 8 | Diskussion | 6–8 | Noch nicht geschrieben |
| 9 | Fazit und Ausblick | 2–3 | Noch nicht geschrieben |
| | **Gesamt** | **~60–80** | |

---

# KAPITEL 1: Einleitung

## 1.1 Inhalt und Aufbau

**Umfang:** 2–3 Seiten
**Ziel:** Den Leser in 5 Minuten abholen — Problem, Lücke, Beitrag, Aufbau.

### Abschnitt 1: Problemstellung (~0,5 Seiten)

**Was du schreiben musst:**
Finanzkennzahlen sind das zentrale Instrument der Unternehmensanalyse — Investoren, Analysten und Manager nutzen sie, um Unternehmen zu bewerten und Entscheidungen zu treffen. Die meisten Studien betrachten Kennzahlen als statische Größen oder untersuchen ihre Niveaus (z.B. "Unternehmen mit hohem ROA performen besser"). Deutlich weniger erforscht ist die *Dynamik* dieser Kennzahlen: Wie schnell korrigieren sich Veränderungen? Gibt es systematische Unterschiede zwischen Kennzahlentypen? Und was bestimmt, ob ein Unternehmen volatile oder stabile Kennzahlen hat?

**Konkreter Einstieg (Vorschlag):**
Beginne mit einem konkreten Beispiel — z.B. Molson Coors (TAP) vs. Qualcomm (QCOM) aus deinem FF1-Anhang. Zwei Unternehmen, zwei komplett unterschiedliche Dynamikmuster. Das macht die Forschungsfrage greifbar.

**Schlüsselbegriffe einführen:**
- Mean-Reversion (Rückkehr zur Normalität)
- Quartalsveränderungen vs. Niveaus
- Dynamik-Profil eines Unternehmens

### Abschnitt 2: Forschungsfragen (~0,5 Seiten)

Die drei Forschungsfragen mit je 1–2 Sätzen Erläuterung:

> **FF1:** Weisen Finanzkennzahlen systematische, messbare Unterschiede in ihrem Quartals-zu-Quartals-Veränderungsverhalten auf?

→ Gibt es eine Hierarchie der Dynamik? Verhalten sich Profitabilitätskennzahlen anders als Bilanzkennzahlen?

> **FF2:** Wie hängen die Dynamikmuster verschiedener Finanzkennzahlen zusammen, und wie manifestieren sie sich in Phasen erhöhter Marktvolatilität?

→ Bewegen sich die Dynamiken als Block oder unabhängig? Haben die Muster prädiktive Kraft für Krisenreaktionen?

> **FF3:** Welche externen Strukturmerkmale — Branche, Unternehmensgröße, Kapitalstruktur — beeinflussen die Zuordnung eines Unternehmens zu einem Dynamiktyp?

→ Ist die Klassifikation ökonomisch erklärbar oder ein statistisches Artefakt?

### Abschnitt 3: Aufbau der Arbeit (~0,5 Seiten)

Kurzer "Fahrplan" — welches Kapitel macht was und warum in dieser Reihenfolge. Hier den roten Faden explizit machen:
- Kap. 2+3: Theoretisches Fundament und Literaturlücke
- Kap. 4: Methodische Entscheidungen und Begründungen
- Kap. 5: FF1 (das Phänomen etablieren)
- Kap. 6: FF2 (das Phänomen intern verstehen)
- Kap. 7: FF3 (das Phänomen extern validieren)
- Kap. 8+9: Einordnung, Grenzen, Ausblick

### Quellen für Kapitel 1

Keine formale Literatur nötig — die Einleitung verweist auf spätere Kapitel. Höchstens 1–2 Referenzen zur Motivation (z.B. Dichev & Tang 2009 für Earnings-Dynamik als Forschungsfeld).

### To-Do für Kapitel 1

- [ ] Einstiegsbeispiel wählen (TAP vs. QCOM oder anderes)
- [ ] Forschungsfragen final formulieren (exakter Wortlaut für gesamte Arbeit)
- [ ] Aufbau-Absatz schreiben (erst nachdem Kap. 2–8 in Gliederung stehen)

---

# KAPITEL 2: Theoretische Grundlagen

## 2.1 Inhalt und Aufbau

**Umfang:** 8–10 Seiten
**Ziel:** Dem Leser alles geben, was er braucht, um Kapitel 4 (Methodik) und Kapitel 5–7 (Ergebnisse) zu verstehen — nicht mehr, nicht weniger. Dieses Kapitel beantwortet: "Was muss ich wissen, um die Arbeit zu verstehen?"

**Stollhoffs Feedback hierzu:** Er hat Grundlagen nicht explizit kritisiert, aber das Fehlen von Modellgleichungen und Interpretationsbezügen deutet darauf hin, dass ein solides Theoriekapitel die Arbeit stark verbessern würde.

### Abschnitt 2.1: Finanzkennzahlen und ihre ökonomische Bedeutung (~2 Seiten)

**Was du schreiben musst:**

**A) Die sieben Kennzahlen und ihre Berechnung:**
Tabelle mit allen 7 Kennzahlen, ihrer Formel, und einer Zeile zur ökonomischen Interpretation.

| Kennzahl | Formel | Misst |
|----------|--------|-------|
| ROA | Nettoergebnis / Bilanzsumme | Gesamtkapitalrentabilität |
| ROE | Nettoergebnis / Eigenkapital | Eigenkapitalrentabilität |
| EBIT-Marge | EBIT / Umsatz | Operative Profitabilität |
| FCF-Marge | Free Cashflow / Umsatz | Cashflow-Generierung |
| Current Ratio | Umlaufvermögen / kurzfr. Verbindlichkeiten | Kurzfristige Zahlungsfähigkeit |
| Debt-to-Equity | Fremdkapital / Eigenkapital | Verschuldungsgrad |
| EK-Quote | Eigenkapital / Bilanzsumme | Eigenfinanzierungsgrad |

**B) Die drei Kategorien und warum sie sich unterschiedlich verhalten:**
- **Profitabilität** (ROA, ROE, EBIT-Marge, FCF-Marge): Marktgetrieben. Umsatz und Kosten schwanken mit Nachfrage, Wettbewerb, Konjunktur. Quartalsveränderungen enthalten temporäre Effekte, die sich systematisch zurückbilden.
- **Liquidität** (Current Ratio): Hybrid — teilweise operativ (Lagerzyklen, Zahlungsziele), teilweise managementgesteuert (Kreditlinien).
- **Kapitalstruktur** (D/E, EK-Quote): Managementgesteuert. Finanzierungsentscheidungen sind diskret (Anleiheemission, Buyback), nicht kontinuierlich.

→ WICHTIG: Diese theoretische Dreiteilung wird in Kap. 5 empirisch bestätigt. Das ist der rote Faden.

**C) DuPont-Zerlegung und Wechselwirkungen:**
ROE = ROA × Leverage-Faktor. Diese mechanische Beziehung erklärt, warum ROE und D/E in der Volatilität korrelieren (ρ = 0.82 in FF2) — das ist kein ökonomisches Signal, sondern eine Formelkonsequenz. Referenz: Nissim & Penman (2001).

**Quellen für 2.1:**
- Nissim & Penman (2001) — DuPont-Framework, Kennzahlenauswahl
- Standard-Lehrbücher (Penman, Palepu/Healy/Peek) — Definitionen
- **LÜCKE:** Du brauchst ein Lehrbuch als Standardreferenz für die Kennzahl-Definitionen. Empfehlung: Penman "Financial Statement Analysis and Security Valuation" oder Palepu/Healy "Business Analysis and Valuation".

### Abschnitt 2.2: Mean-Reversion in der Finanztheorie (~2 Seiten)

**Was du schreiben musst:**

**A) Das Konzept Mean-Reversion:**
- Definition: Die Tendenz einer Variablen, nach Abweichungen zu einem langfristigen Mittelwert zurückzukehren
- Ökonomische Begründung: Wettbewerb (hohe Renditen ziehen Konkurrenz an → Renditen sinken), operative Normalisierung (Einmaleffekte verschwinden), regulatorische Kräfte
- Unterscheidung: Mean-Reversion des *Niveaus* (klassisch) vs. Mean-Reversion der *Veränderungen* (dein Ansatz)

**B) Mean-Reversion auf Niveaus vs. auf Differenzen:**
Das ist DER theoretische Kernpunkt deiner Arbeit und adressiert direkt Stollhoffs Feedback.

- **Auf Niveaus:** Y(t) = c + φ₁ · Y(t−1) + ε(t). Hier misst φ₁, wie schnell das Niveau zum Langfristmittel zurückkehrt. Hoher φ₁ (nahe 1) = persistentes Niveau.
- **Auf ersten Differenzen:** ΔY(t) = c + φ₁ · ΔY(t−1) + ε(t). Hier misst φ₁, wie schnell sich *Veränderungen* korrigieren. Negativer φ₁ = überdurchschnittliche Veränderung wird im Folgequartal teilweise rückgängig gemacht.

Diese Unterscheidung ist fundamental für das Verständnis deiner Ergebnisse:
- Eigenkapitalquote: Hohes Level-φ₁ (0.93) = sehr persistentes Niveau. Aber Diff-φ₁ ≈ 0 = die quartalsweisen Änderungen sind zufällig.
- ROA: Moderates Level-φ₁ (0.36) = Niveau schwankt. Aber Diff-φ₁ = −0.43 = die Schwankungen korrigieren sich systematisch.

→ Beide Perspektiven zusammen ergeben erst das volle Bild. Das muss theoretisch motiviert werden.

**C) Stationarität und warum erste Differenzen:**
- Unit Root vs. Stationarität (kurz, nicht zu technisch)
- Argument: Erste Differenzen stellen Stationarität sicher, ohne Annahmen über die Integrationsordnung
- Trade-off: Einheitliche Transformation für alle 7 Kennzahlen ermöglicht Vergleichbarkeit (Uniformitätsargument aus METHODIK_DISKUSSION.md)

**Quellen für 2.2:**
- Dichev & Tang (2009) — Hauptquelle für Earnings-Mean-Reversion, AR(1)-Ansatz
- Fairfield & Yohn (2001) — Validiert Differenzen als informativer als Niveaus
- **LÜCKE:** Standardreferenz für Stationarität/Unit Root in Finanz-Paneldaten. Empfehlung: Hamilton "Time Series Analysis" oder Wooldridge "Introductory Econometrics" für den theoretischen Rahmen.

### Abschnitt 2.3: Autoregressive Modelle (~2 Seiten)

**Was du schreiben musst:**

**A) Das AR(1)-Modell — formale Darstellung:**
Alle vier Varianten deiner Arbeit mit expliziter Gleichung, Parameterinterpretation und Annahmen.

**Hauptmodell (diff1):**
> ΔY(t) = c + φ₁ · ΔY(t−1) + ε(t)
> - ΔY(t) = Y(t) − Y(t−1) (Quartalsveränderung der Kennzahl)
> - c = Drift-Konstante (mittlere Veränderung)
> - φ₁ = Autokorrelationskoeffizient der Veränderungen
> - ε(t) ~ WN(0, σ²) (White-Noise-Fehlerterm)
> - Interpretation: φ₁ < 0 → Mean-Reversion der Veränderungen; φ₁ ≈ 0 → unabhängige Veränderungen

**Levels-Variante:**
> Y(t) = c + φ₁ · Y(t−1) + ε(t)
> - Misst Niveaupersistenz statt Veränderungsdynamik
> - Dient als komplementäre Perspektive: Hoher φ₁ auf Levels + niedriger |φ₁| auf Diffs = persistentes, aber wenig dynamisches Niveau

**AR(2) auf Differenzen:**
> ΔY(t) = c + φ₁ · ΔY(t−1) + φ₂ · ΔY(t−2) + ε(t)
> - Testet, ob ein Lag ausreicht oder zusätzliche Korrekturstruktur besteht
> - Ergebnis vorwegnehmen: φ₂ ist bei Profitabilität relevant, bei Bilanzstruktur nicht

**Saisonale Differenzen (diff4):**
> Δ₄Y(t) = Y(t) − Y(t−4), dann AR(1): Δ₄Y(t) = c + φ₁ · Δ₄Y(t−1) + ε(t)
> - Eliminiert saisonale Muster (Q1-zu-Q1-Vergleich statt Q1-zu-Q4)
> - Testet Robustheit gegenüber Saisonalität

**B) Warum AR und nicht VAR, GARCH, oder Strukturbruchmodelle?**
- VAR: Love & Zicchino (2006) zeigen Panel-VAR als Referenz. Du entscheidest dagegen, weil die cross-kategorialen φ₁-Korrelationen < 0.10 sind → wenig dynamische Kausalität zwischen den Schichten
- GARCH: Modelliert bedingte Varianz, aber deine Frage ist die Autokorrelation der *Mittelwerte* der Veränderungen, nicht die Varianzstruktur
- Strukturbruchmodelle: Deine Event-Analyse (FF2) adressiert Strukturbrüche datengetrieben statt parametrisch

→ Das ist die "Warum dieses Modell?"-Begründung, die Stollhoff fordert.

**Quellen für 2.3:**
- Love & Zicchino (2006) — VAR-Referenz (Abgrenzung)
- Dichev & Tang (2009) — AR(1) auf Earnings als methodischer Vorläufer
- Hamilton "Time Series Analysis" — AR-Modell-Theorie
- **LÜCKE:** Ein Standard-Ökonometrie-Lehrbuch für die formale AR-Modell-Herleitung. Wooldridge oder Greene wären geeignet.

### Abschnitt 2.4: Quadrantenklassifikation als Typologierahmen (~1,5 Seiten)

**Was du schreiben musst:**

**A) Die zwei Dimensionen:**
- φ₁ (Mean-Reversion-Stärke) als vertikale Achse
- σ(ΔY) (Änderungsvolatilität) als horizontale Achse
- Warum gerade diese zwei? → Sie messen unterschiedliche Dinge (FF3 zeigt: σ ist größenabhängig, φ₁ nicht) und spannen einen interpretierbaren Raum auf

**B) Die vier Quadranten:**
| Quadrant | φ₁ | σ(ΔY) | Ökonomische Interpretation |
|----------|-----|-------|---------------------------|
| Korrektiv-Stabil | stark negativ | niedrig | Vorhersagbar stabil. Veränderungen sind klein und korrigieren sich. Typisch: reife, diversifizierte Unternehmen. |
| Korrektiv-Volatil | stark negativ | hoch | Große Ausschläge, die sich aber systematisch zurückbilden. Typisch: zyklische Branchen mit Korrekturmechanismen. |
| Persistent-Stabil | nahe 0 | niedrig | Langsame, gleichmäßige Drift. Veränderungen sind klein, aber bleiben bestehen. Typisch: Unternehmen mit Trägheits-Kennzahlen. |
| Persistent-Volatil | nahe 0 | hoch | Unvorhersagbar. Große Veränderungen ohne Korrektur. Höchstes Risikoprofil. |

**C) Median-Split als Trennmechanismus:**
- Einfacher, nachvollziehbarer Ansatz
- Limitation: Willkürliche Grenzziehung (Stollhoff hat das als Schwäche identifiziert)
- Robustheitscheck: K-Means bestätigt die Hauptdifferenzierung (Kap. 7)

**D) Mechanische Abhängigkeit φ₁ × σ — vorab entkräften:**
Theoretisch könnte höhere Volatilität automatisch stärkere Mean-Reversion erzeugen. Empirisch ist die Korrelation schwach (|ρ| < 0.19 bei Profitabilität). Monte-Carlo-Benchmark zeigt: Reale Korrelation deutlich unter mechanischem Erwartungswert. Die Dimensionen sind trennbar.

**Quellen für 2.4:**
- Dzuba & Krylov (2021) — Cluster-Analyse als methodische Referenz
- **LÜCKE:** Literatur zu Median-Split-Ansätzen in der empirischen Finanzforschung. Gibt es methodische Diskussionen zu Vor-/Nachteilen? Alternativ: Referenz auf Fama & French Portfolio-Sorts als verwandtes Konzept.

### To-Do für Kapitel 2

- [ ] Lehrbuch-Referenz für Kennzahl-Definitionen beschaffen (Penman oder Palepu)
- [ ] Lehrbuch-Referenz für AR-Modelle/Stationarität beschaffen (Hamilton oder Wooldridge)
- [ ] Formale Gleichungen sauber aufschreiben (LaTeX-ready)
- [ ] Abschnitt 2.2 B) über Niveaus vs. Differenzen ausformulieren (Kernpunkt!)
- [ ] Median-Split-Literatur recherchieren
- [ ] Prüfen: Gibt es eine theoretische Arbeit, die die Drei-Kategorien-Unterscheidung (operativ vs. hybrid vs. diskret) formal begründet? Das wäre sehr wertvoll.

---

# KAPITEL 3: Stand der Forschung

## 3.1 Inhalt und Aufbau

**Umfang:** 6–8 Seiten
**Ziel:** Zeigen, was die Literatur bereits weiß, wo die Lücke ist, und wie deine Arbeit diese Lücke füllt. Nicht: eine Auflistung von Quellen. Stattdessen: eine Argumentation, die zu deinen Forschungsfragen hinführt.

**Stollhoffs Feedback:** "Literatureinordnung" war ein expliziter Punkt. Der Professor will sehen, dass du weißt, in welchem Forschungsfeld du dich bewegst.

### Abschnitt 3.1: Earnings Persistence und Mean-Reversion (~2 Seiten)

**Was du schreiben musst:**

**A) Die klassische Earnings-Persistence-Literatur:**
- Sloan (1996) — Accruals und Cashflow-Komponenten haben unterschiedliche Persistenz
- Dechow (1994) — Warum Accrual-basierte Kennzahlen (EBIT) andere Dynamik zeigen als Cashflow-basierte (FCF). Timing von Einnahmen vs. tatsächliche Zahlungen.
- Dichev & Tang (2009) — **Hauptquelle.** AR(1) auf Earnings, negative Beziehung zwischen Volatilität und Vorhersagbarkeit. Ihre Ergebnisse auf S. 162–167 sind dein direkter Benchmark.

**B) Was die Literatur NICHT macht (= deine Lücke):**
- Fokus auf Earnings (ein Aggregat), nicht auf ein Panel von 7 verschiedenen Kennzahlentypen
- Analyse auf Niveaus, nicht auf Differenzen (dein Beitrag: Differenzen-Perspektive)
- Keine systematische Vergleichsanalyse zwischen Profitabilität, Liquidität und Kapitalstruktur
- Keine Quadrantenklassifikation der Dynamik-Typen

→ Hier entsteht die Forschungslücke: "Die Literatur untersucht Earnings-Persistenz auf Niveaus. Die Dynamik der *Veränderungen* verschiedener Kennzahlentypen — und ob diese systematisch unterschiedlich ist — ist kaum erforscht."

**Quellen:**
- Dichev & Tang (2009) — VORHANDEN, PDF geladen
- Dechow (1994) — VORHANDEN, PDF geladen (braucht ggf. Uni-Zugang)
- Sloan (1996) — **LÜCKE: FEHLT.** Muss beschafft werden. "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?" Accrual-Anomaly-Papier. Extrem häufig zitiert, quasi unverzichtbar.
- **LÜCKE:** Fama & French (2000) "Forecasting Profitability and Earnings" — untersucht Mean-Reversion von Profitabilität direkt. Fehlt in deiner Liste.

### Abschnitt 3.2: Firmengröße und Kennzahlen-Dynamik (~1,5 Seiten)

**Was du schreiben musst:**

**A) Fama & French (1992) und der Größeneffekt:**
- Kleinere Unternehmen haben höhere Renditen, aber auch höhere Volatilität
- Dein FF3-Befund erweitert das: Größe (Mitarbeiter) korreliert mit σ(ΔY) bis ρ = −0.53, aber NICHT mit φ₁
- Das bedeutet: Größe erklärt *wie stark* Kennzahlen schwanken, aber nicht *wie schnell* sie korrigieren

**B) Diversifikationshypothese:**
- Mehr Mitarbeiter → mehr Standorte/Produkte/Kunden → mehr Glättung
- Operationale Größe (Employees) stärker als finanzielle Größe (MarketCap)
- Konsistent mit deinen Daten (ρ_Employees > ρ_MarketCap für σ)

**Quellen:**
- Fama & French (1992) — VORHANDEN
- **LÜCKE:** Eine Arbeit zur Diversifikationshypothese in Bezug auf Earnings-Volatilität. Mögliche Kandidaten: Comin & Philippon (2006) "The Rise in Firm-Level Volatility" oder Bushman et al.

### Abschnitt 3.3: Brancheneffekte und regulatorische Einflüsse (~1,5 Seiten)

**Was du schreiben musst:**

**A) Branchenspezifische Kennzahlen-Dynamik:**
- Eljelly (2004) — Liquiditäts-Profitabilitäts-Trade-off. Korrelation auf Niveaus, aber deine Arbeit zeigt Unabhängigkeit auf Dynamik-Ebene (FF2). Das ist ein wichtiger Kontrast.
- Regulierung als Dynamik-Treiber: Utilities mit Basel III/Solvency II als Erklärung für Mean-Reversion bei Kapitalstruktur

**B) Leverage-Effekt:**
- Christie (1982) — Stochastisches Verhalten von Aktienvarianz. Erklärt die ROE×D/E-Volatilitätskopplung (ρ = 0.82 in deiner FF2-Analyse) als mechanischen Effekt.
- Nissim & Penman (2001) — DuPont-Zerlegung als formaler Rahmen

**Quellen:**
- Eljelly (2004) — VORHANDEN
- Christie (1982) — VORHANDEN (braucht ggf. Uni-Zugang)
- Nissim & Penman (2001) — VORHANDEN
- **LÜCKE:** Regulierungseffekte auf Finanz-Kennzahlen — z.B. eine Arbeit zu Basel III und Bankbilanzen

### Abschnitt 3.4: Cluster-Analyse und Unternehmensklassifikation (~1 Seite)

**Was du schreiben musst:**

**A) Vorarbeiten zur Kennzahlen-basierten Unternehmensklassifikation:**
- Dzuba & Krylov (2021) — K-Means auf Finanzkennzahlen. Methodische Referenz für deinen Robustheitscheck.
- Abgrenzung: Sie clustern auf *Niveaus*, du auf *Dynamik-Parametern* (φ₁, σ)

**Quellen:**
- Dzuba & Krylov (2021) — VORHANDEN
- **LÜCKE:** Gibt es Arbeiten, die AR-Parameter als Clustering-Features verwenden? Das wäre ein direkter Vorläufer.

### Abschnitt 3.5: Forschungslücke und Beitrag dieser Arbeit (~1 Seite)

**Was du schreiben musst:**

Synthese der Lücken aus 3.1–3.4:

1. **Earnings-Persistenz ist gut erforscht, Veränderungs-Dynamik nicht.** Die Literatur misst wie persistent *Niveaus* sind. Du misst wie schnell sich *Veränderungen* korrigieren. Das ist konzeptionell verschieden.

2. **Einzelne Kennzahlen sind erforscht, systematische Vergleiche über Typen hinweg nicht.** Dichev & Tang untersuchen Earnings. Eljelly untersucht Liquidität. Niemand vergleicht 7 Kennzahlen über 3 Kategorien hinweg mit derselben Methode auf demselben Datensatz.

3. **Dynamik-Profile als Unternehmenscharakteristik sind neu.** Die Quadrantenklassifikation (φ₁ × σ) existiert in dieser Form nicht in der Literatur. Die externe Validierung (FF3) zeigt, dass sie ökonomisch sinnvoll ist.

→ "Diese Arbeit schließt die Lücke, indem sie..."

### Quellen-Gesamtübersicht mit Einordnung

| # | Quelle | Kapitel | Kernnutzung | Status |
|---|--------|---------|-------------|--------|
| 1 | Dechow (1994) | 2.1, 3.1 | Accruals vs. Cashflow-Dynamik, erklärt EBIT≠FCF | PDF vorhanden (Uni-Zugang?) |
| 2 | Dzuba & Krylov (2021) | 2.4, 3.4 | K-Means-Referenz für Robustheitscheck | PDF vorhanden |
| 3 | Dichev & Tang (2009) | 2.2, 3.1, 4 | **Hauptquelle.** AR(1)-Benchmark, Diffs-Ansatz | PDF vorhanden |
| 4 | Love & Zicchino (2006) | 2.3 | VAR-Referenz (Abgrenzung: warum nicht VAR) | PDF vorhanden |
| 5 | Eljelly (2004) | 3.3 | Liquiditäts-Profitabilitäts-Trade-off (Kontrast) | PDF vorhanden |
| 6 | Nissim & Penman (2001) | 2.1, 3.3 | DuPont-Framework, Leverage-Mechanik | PDF vorhanden |
| 7 | Fama & French (1992) | 3.2, 7 | Größeneffekt als Vergleich zu FF3-Befunden | PDF vorhanden |
| 8 | Christie (1982) | 3.3 | Leverage-Effekt, ROE×D/E-Kopplung | PDF vorhanden (Uni-Zugang?) |
| 9 | Wave-Particle (2024) | 8 (Diskussion) | Thematische Analogie, NICHT methodisch | PDF vorhanden |
| 10 | Fairfield & Yohn (2001) | 2.2, 4 | Validiert Differenzen > Niveaus | PDF vorhanden |
| **NEU** | Sloan (1996) | 3.1 | Accrual-Anomaly, Earnings-Persistence | **FEHLT — beschaffen** |
| **NEU** | Fama & French (2000) | 3.1 | Mean-Reversion Profitabilität | **FEHLT — beschaffen** |
| **NEU** | Hamilton (1994) oder Wooldridge | 2.2, 2.3 | AR-Theorie, Stationarität (Lehrbuch) | **FEHLT — beschaffen** |
| **NEU** | Penman (Lehrbuch) | 2.1 | Kennzahl-Definitionen (Standardreferenz) | **FEHLT — beschaffen** |
| **NEU** | Regulierung (Basel III) | 3.3, 5, 7 | Erklärung für Utilities/FinServ-Anomalie | **FEHLT — recherchieren** |
| ? | "Ep" (unbekannt) | ? | Aus NotebookLM-Liste, noch nicht identifiziert | **FEHLT — identifizieren** |

**Quellen, die MEHRFACH relevant werden:**
- Dichev & Tang (2009): Kap. 2, 3, 4, 5 — dein wichtigstes Papier
- Nissim & Penman (2001): Kap. 2, 3, 6 — DuPont und Leverage
- Fama & French (1992): Kap. 3, 7 — Größeneffekt

### To-Do für Kapitel 3

- [ ] **KRITISCH:** Sloan (1996) beschaffen und lesen — unverzichtbar für Earnings-Persistence
- [ ] Fama & French (2000) beschaffen — Mean-Reversion von Profitabilität
- [ ] Dichev & Tang (2009) Seiten 162–167 und 175–178 durcharbeiten (spezifische Benchmarks)
- [ ] "Ep"-Quelle aus NotebookLM identifizieren
- [ ] Literatur zu Median-Split in Finanzforschung recherchieren
- [ ] 1–2 Arbeiten zu regulatorischen Effekten auf Bilanzkennzahlen finden
- [ ] Arbeit zu Diversifikation und Earnings-Volatilität finden (für 3.2)
- [ ] Prüfen: Gibt es Arbeiten, die AR-Parameter als Unternehmenscharakteristik nutzen?

---

# KAPITEL 4: Methodik

## 4.1 Inhalt und Aufbau

**Umfang:** 10–12 Seiten
**Ziel:** Jede methodische Entscheidung transparent und begründet darstellen. Der Leser muss nach diesem Kapitel wissen: Was wird gemacht, warum so, und was wäre die Alternative gewesen.

**Stollhoffs Feedback hierzu:** Sein zentraler Punkt. "Modellwahl begründen", "Gleichungen zeigen", "wie hängen die Varianten zusammen". Dieses Kapitel ist das Herzstück der methodischen Arbeit.

**Hybrider Ansatz:** Kapitel 4 enthält die zentrale, FF-übergreifende Methodik. FF-spezifische Erweiterungen (z.B. Event-Analyse für FF2, χ²-Tests für FF3) kommen in die jeweiligen Ergebniskapitel als kurze Methodik-Einschübe.

### Abschnitt 4.1: Datenbasis (~2 Seiten)

**Was du schreiben musst:**

**A) Datenquelle und Universum:**
- S&P 1500 (Composite Index): Large-Cap, Mid-Cap, Small-Cap US-Unternehmen
- Quartalsberichte (10-Q/10-K): 7 Finanzkennzahlen pro Quartal
- Zeitraum: Q1/2000–Q4/2024 (100 Quartale, 25 Jahre)
- Datenquelle benennen (woher kommen die Rohdaten?)

**B) Filterkette (konkret und transparent):**

| Schritt | Aktion | Vorher | Entfernt | Nachher | Begründung |
|---------|--------|:------:|:--------:|:-------:|-----------|
| 1 | Ticker-Universum (Schnittmenge BS/IS/CF) | – | – | 5.871 | Nur Unternehmen mit allen 3 Statements |
| 2a | Sektor-Filter (Financial Services) | 5.871 | 883 | 4.988 | Regulierte Bilanzen verzerren Vergleichbarkeit |
| 2b | ADR-Filter | 4.988 | 646 | 4.342 | Nur US-GAAP-Berichterstatter |
| 3 | Vollständigkeitsfilter (100 Quartale) | 4.342 | 3.366 | 976 | Minimum 25 Jahre für stabile AR-Schätzung |
| 4 | NaN/Qualitätsfilter | 976 | 44 | 932 | Fehlende Werte, Datenqualitätsprobleme |

**C) Survivorship Bias — explizit adressieren:**
- Der Vollständigkeitsfilter entfernt 77% der Ticker
- Die verbleibenden 932 sind die "Überlebenden" seit 2000
- Robustheitscheck in Kap. 5 mit 80Q (1.231), 60Q (1.855), 40Q (2.356) Unternehmen
- Ergebnis vorwegnehmen: φ₁-Mediane für Profitabilität weichen < 3% ab

**D) USGAAP vs. IFRS:**
- Alle Unternehmen berichten nach US-GAAP (ADR-Filter entfernt ausländische)
- Offener Punkt: Prof. Steglich wurde gefragt → Feedback einarbeiten

**E) Datenaufbereitung:**
- Outlier-Detection (welche Methode? Winsorizing? Auf welchem Perzentil?)
- NaN-Behandlung (Interpolation? Ausschluss?)
- Saisonale Bereinigung (nein — erste Differenzen adressieren Saisonalität, Δ₄Y als Check)

→ WICHTIG: Hier transparent alles dokumentieren. Replizierbarkeit ist ein Qualitätsmerkmal.

**Quellen für 4.1:**
- Eigene Datenaufbereitung (Code referenzieren)
- Fama & French (1992) — Begründung für Größen-/Branchenvergleiche
- **LÜCKE:** Referenz für Winsorizing/Outlier-Behandlung in Paneldaten

### Abschnitt 4.2: AR(1)-Modellspezifikation (~3 Seiten)

**Was du schreiben musst — DAS KERNSTÜCK:**

**A) Warum AR(1) auf ersten Differenzen?**

Die Argumentationskette (die du im Meeting am Donnerstag am besten an die Tafel schreibst):

1. **Forschungsfrage definiert das Ziel:** FF1 fragt nach "Quartals-zu-Quartals-Veränderungsverhalten". Das Ziel ist also die Modellierung der *Veränderungen*, nicht der *Niveaus*.

2. **Erste Differenzen als Transformation:** ΔY(t) = Y(t) − Y(t−1) transformiert die Zeitreihe von Niveaus in Veränderungen. Vorteil: Sichert Stationarität, hat direkte ökonomische Interpretation ("um wie viel hat sich die Kennzahl dieses Quartal verändert?").

3. **AR(1) als Modell:** ΔY(t) = c + φ₁ · ΔY(t−1) + ε(t). Einfachstes Modell, das die Ein-Schritt-Autokorrelation der Veränderungen erfasst. Parsimonie-Argument: Wenn AR(1) die Muster bereits erklärt, braucht man kein komplexeres Modell.

4. **Warum nicht höhere Ordnungen?** AR(2) wird als Robustheitscheck getestet. Ergebnis: φ₂ ist bei Profitabilität relevant (R² steigt von 0.19 auf 0.29), bei Bilanzstruktur nicht. AR(1) ist konservativer und die qualitative Aussage bleibt gleich.

5. **Warum nicht Levels als Hauptmodell?** Levels messen etwas anderes (Niveaupersistenz). Außerdem: Profitabilitätskennzahlen auf Niveaus sind potenziell nicht-stationär, was OLS-Schätzer verzerrt. Differenzen lösen das Problem.

6. **Warum nicht Δ₄Y (saisonale Differenzen)?** Vorzeichenwechsel zu positivem φ₁ zeigt: Jahresveränderungen sind persistent. Das ist eine andere Frage als "wie schnell korrigieren sich Quartalsveränderungen?". Δ₄Y als Robustheitscheck zeigt, dass die Rangordnung stabil bleibt.

**B) Einheitliche Transformation für alle 7 Kennzahlen:**
Das Uniformitätsargument aus METHODIK_DISKUSSION.md: Vergleichbarkeit der φ₁-Koeffizienten erfordert identische Transformation. Trade-off explizit benennen.

**C) Schätzung:**
- OLS pro Unternehmen und Kennzahl (932 × 7 = 6.524 Regressionen)
- Keine Panel-Regression — bewusste Entscheidung: Individuelle Schätzung erlaubt Heterogenität
- Signifikanz: t-Test auf φ₁ ≠ 0, p < 0.05
- R² als Maß für Modellgüte

**Quellen für 4.2:**
- Dichev & Tang (2009) — AR(1)-Vorläufer
- Fairfield & Yohn (2001) — Differenzen > Niveaus
- METHODIK_DISKUSSION.md Abschnitte 2 und 5 — direkt verwertbar
- **LÜCKE:** Referenz für individuelle OLS vs. Panel-Regression als Designentscheidung

### Abschnitt 4.3: Quadrantenklassifikation (~1,5 Seiten)

**Was du schreiben musst:**

**A) Konstruktion:**
- Zwei Parameter pro Unternehmen-Kennzahl-Kombination: φ₁ und σ(ΔY)
- Median-Split: Werte über/unter dem Gesamtmedian → 4 Quadranten
- 932 × 7 = 6.524 Zuweisungen

**B) Warum Median-Split und nicht K-Means direkt?**
- Interpretierbarkeit: Die Labels (Korrektiv/Persistent × Stabil/Volatil) sind direkt aus den Dimensionen abgeleitet
- Transparenz: Jeder kann die Zuordnung nachvollziehen
- Limitation: Willkürliche Grenzziehung, keine "natürliche" Clustergröße
- K-Means als Robustheitscheck in Kap. 7

**C) Mechanische Abhängigkeit entkräften:**
- Monte-Carlo-Simulation zeigt: Reale φ₁-σ-Korrelation (|ρ| < 0.19 für Profitabilität) deutlich unter mechanischem Benchmark (ρ = −0.75)
- Alle vier Quadranten annähernd gleichverteilt (χ²-Test n.s.)
- Verweis auf METHODIK_DISKUSSION.md Abschnitt 1

### Abschnitt 4.4: Robustheitsdesign (~2 Seiten)

**Was du schreiben musst:**

Übersicht über alle Robustheitschecks, die in Kap. 5–7 berichtet werden:

| Check | Was wird getestet | Ergebnis (kurz) | Kapitel |
|-------|-------------------|-----------------|---------|
| AR-Varianten (Levels, AR(2), Δ₄Y) | Modellabhängigkeit | Hierarchie stabil | 5 |
| Variable Stichproben (80Q–40Q) | Survivorship Bias | φ₁ Abweichung < 3% | 5 |
| Financial Services | Sektorabhängigkeit | Profitabilität identisch, Bilanz verschoben | 7 |
| K-Means | Quadranten-Validierung | Bestätigt Volatilitäts-Hauptachse | 7 |
| Monte-Carlo | φ₁-σ-Unabhängigkeit | Reale Korrelation << mechanische | 4 |

### Abschnitt 4.5: FF-spezifische Methoden (Vorschau) (~1 Seite)

Kurzer Überblick über Methoden, die nur in einzelnen FFs verwendet werden:

**FF2-spezifisch (Details in Kap. 6):**
- Spearman-Korrelation für φ₁ und σ cross-sektional
- Cramér's V für Quadrantenüberschneidungen
- Datengetriebene Peak-Identifikation (90. Perzentil rollierender Querschnittsvolatilität)
- Mann-Whitney U-Tests und Kruskal-Wallis für Event-Reaktionen

**FF3-spezifisch (Details in Kap. 7):**
- χ²-Tests: Sektor × Quadrant
- Spearman-Korrelation: Größe × (φ₁, σ)
- K-Means auf AR-Features (k=2)
- Konsistenz-Scores für Unternehmensprofile

### To-Do für Kapitel 4

- [ ] **KRITISCH:** Argumentationskette "Warum AR(1) auf Diffs" sauber ausformulieren
- [ ] Datenquelle benennen (woher kommen die Rohdaten? Bloomberg? Compustat? SimFin?)
- [ ] Outlier-Behandlung und Winsorizing dokumentieren (aus Code nachvollziehen)
- [ ] Referenz für individuelle OLS vs. Panel-Regression beschaffen
- [ ] Monte-Carlo-Ergebnisse formal aufschreiben
- [ ] Formel-Darstellung in LaTeX vorbereiten
- [ ] Prüfen: Sind alle 4 Modellvarianten im Code sauber implementiert? (ar_features_all.csv)

---

# Zusammenfassung: Was als Nächstes?

## Kritischer Pfad

Die folgenden Aufgaben blockieren den Schreibfortschritt:

1. **Literatur beschaffen** (Sloan 1996, Fama & French 2000, Lehrbuch AR-Theorie, Lehrbuch Kennzahlen)
   → Ohne diese Quellen sind Kap. 2 und 3 nicht schreibbar
   → Zeitbedarf: 1–2 Tage (Uni-Bibliothek, Sci-Hub)

2. **Modell-Gleichungen formalisieren** (Kap. 2.3 + 4.2)
   → Stollhoffs zentraler Punkt
   → Kann sofort geschrieben werden, Kontext ist vollständig
   → Zeitbedarf: 2–3 Stunden

3. **Datenquelle und Aufbereitung dokumentieren** (Kap. 4.1)
   → Muss aus dem Code nachvollzogen werden
   → Zeitbedarf: 1–2 Stunden

## Empfohlene Schreibreihenfolge

| Schritt | Kapitel | Warum jetzt | Vorbedingung |
|---------|---------|-------------|-------------|
| 1 | Kap. 4.2 (Modellspezifikation) | Stollhoff-Feedback, Meeting-Vorbereitung | Keine — Kontext vorhanden |
| 2 | Kap. 2.2 + 2.3 (Mean-Reversion + AR-Theorie) | Fundament für 4.2 | Lehrbuch-Referenz (kann parallel laufen) |
| 3 | Kap. 4.1 (Datenbasis) | Dokumentation, muss sowieso rein | Code-Review |
| 4 | Kap. 3 (Literatur) | Braucht die meiste Recherche | Alle fehlenden Quellen beschafft |
| 5 | Kap. 1 (Einleitung) | Schreibt sich leichter, wenn 2–4 stehen | Kap. 2–4 zumindest als Entwurf |

## Offene methodische Fragen für das Meeting am Donnerstag

1. **Granger-Kausalität:** Durchführen oder die niedrigen cross-kategorialen Korrelationen als Argument nutzen, dass es nicht nötig ist?
2. **Fama-French-Regression:** Quadrantenzugehörigkeit auf Size/Value/Momentum-Faktoren regressieren — sinnvoll oder Scope-Sprengung?
3. **USGAAP vs. IFRS:** Feedback von Prof. Steglich abwarten?
4. **Δ₄Y Interpretation:** Der Vorzeichenwechsel (positiv auf saisonalen Diffs) — wie stark soll das diskutiert werden?

---

---

# KAPITEL 5: FF1 — Systematische Dynamikmuster von Finanzkennzahlen

## 5.0 Strukturprinzip

**Umfang:** 12–15 Seiten
**Ziel:** Den zentralen empirischen Befund der Arbeit präsentieren — die Drei-Schichten-Hierarchie — und zeigen, dass er robust ist.

**Verbindung zu Kap. 1–4:**
- Kap. 2.2 hat Mean-Reversion auf Niveaus vs. Differenzen theoretisch motiviert → Kap. 5 liefert den empirischen Nachweis
- Kap. 2.4 hat die Quadrantenklassifikation eingeführt → Kap. 5 zeigt sie am Beispiel ROA
- Kap. 4.2 hat das AR(1)-Modell begründet → Kap. 5 wendet es an und berichtet die Ergebnisse
- Kap. 4.4 hat das Robustheitsdesign vorgestellt → Kap. 5.3 setzt es um

**Stollhoffs Feedback adressieren:**
- "Modellgleichungen" → Die Gleichung steht in Kap. 4, hier wird sie *angewendet* und interpretiert
- "Mehr Interpretation" → Jede Schicht wird ökonomisch erklärt, nicht nur beschrieben
- "Diskussion der Schwächen" → Robustheitschecks zeigen Modellunabhängigkeit

**Was Stollhoff bereits gesehen hat (Anhang FF1, 4 Seiten):**
- Methodik-Gleichung, zwei Anschauungsbeispiele (TAP/QCOM), Quadranten-Scatter (ROA)
- Modellvergleichstabelle (diff1/levels/AR(2)/diff4)
- Boxplots der Drei-Schichten-Hierarchie, Signifikanz- und R²-Barplots
- Heatmap Sektor × Kennzahl, Quadrantenverteilung pro Sektor
→ Kap. 5 muss also *über* den Anhang hinausgehen: mehr Text, mehr Interpretation, Literaturvergleich

---

### 5.1 Überblick: Die Drei-Schichten-Hierarchie (~2 Seiten)

**Aufbau:**

**A) Hauptergebnis voranstellen (1 Absatz):**
Die 932 × 7 = 6.524 AR(1)-Schätzungen auf ersten Differenzen zeigen eine klare Dreiteilung der Kennzahlen nach Mean-Reversion-Stärke. Dieses Ergebnis ist der zentrale Befund von FF1.

**B) Die drei Schichten im Detail:**

**Schicht 1 — Profitabilität (ROA, ROE, EBIT-Marge, FCF-Marge):**
| Parameter | Wert | Bedeutung |
|-----------|------|-----------|
| φ₁ Median | −0,43 bis −0,46 | 43–46% einer Quartalsveränderung werden im Folgequartal korrigiert |
| Signifikanzrate | 90–97% | Fast alle Unternehmen zeigen den Effekt |
| R² Median | 0,18–0,21 | AR(1) erklärt ~20% der Varianz — solide für univariates Modell |
| σ(ΔY) Median | 0,017 (ROA) bis 0,165 (FCF) | Interne Spreizung über Volatilität |

Ökonomische Erklärung: Profitabilitätskennzahlen werden durch Marktbedingungen getrieben. Quartalsveränderungen enthalten temporäre Effekte (Einmalerlöse, Timing von Aufträgen, saisonale Schwankungen), die sich im Folgequartal zurückbilden. Der Korrekturmechanismus ist Wettbewerb und operative Normalisierung.

Literatur-Bezug: Dichev & Tang (2009) berichten vergleichbare AR(1)-Koeffizienten für Earnings-Veränderungen → deine Ergebnisse bestätigen und erweitern ihren Befund auf vier separate Profitabilitätskennzahlen.

**Schicht 2 — Liquidität (Current Ratio):**
| Parameter | Wert |
|-----------|------|
| φ₁ Median | −0,17 |
| Signifikanzrate | 46% |
| R² Median | 0,03 |

Ökonomische Erklärung: Liquidität ist ein Hybrid — teilweise operativ (Lagerzyklen, Zahlungszielverhandlungen), teilweise managementgesteuert (Kreditliniennutzung). Die schwache, inkonsistente Mean-Reversion reflektiert diese Mischung.

**Schicht 3 — Kapitalstruktur (D/E, EK-Quote):**
| Parameter | Wert |
|-----------|------|
| φ₁ Median | −0,04 bis −0,09 |
| Signifikanzrate | 19–32% |
| R² Median | 0,008–0,018 |

Ökonomische Erklärung: Kapitalstrukturentscheidungen sind diskret (Anleiheemission, Aktienrückkauf, Kapitalerhöhung). Sie folgen keinem autoregressiven Muster auf Quartalsebene. Das AR(1)-Modell ist hier nicht informativ — was selbst ein Befund ist.

Komplementäre Perspektive (Levels): Auf Niveaus zeigen genau diese Kennzahlen die höchste Persistenz (φ₁ = 0,87–0,93). Die Kapitalstruktur ist extrem stabil im Niveau, aber die seltenen Veränderungen sind quasi-zufällig. → Verweis auf Modellvergleich in 5.3.

**C) Grafik einbinden: Boxplots (bereits vorhanden im Anhang)**
Die Boxplots zeigen die drei Schichten visuell. Im Text darauf eingehen und Leser durch die Grafik führen.

**Verbindung zu Kap. 2:** Die theoretisch motivierte Unterscheidung marktgetrieben vs. managementgesteuert (Abschnitt 2.1) findet hier ihre empirische Bestätigung.

---

### 5.2 Detailanalyse: Kennzahl für Kennzahl (~4–5 Seiten)

**Aufbau:** Pro Kennzahl ein Unterabschnitt. Nicht alle gleich lang — ROA als Leitkennzahl ausführlicher, danach kürzer mit Fokus auf Unterschiede.

**5.2.1 ROA als Leitkennzahl (~1,5 Seiten)**

Warum ROA zuerst: Am stabilsten, engster IQR [−0,50; −0,33], repräsentativ für die gesamte Profitabilitätsschicht. Dient als Referenz für alle weiteren Kennzahlen.

Was rein muss:
- Vollständige Parametertabelle (Mittelwert, Median, Std, IQR, Perzentile)
- Interpretation: "Ein typisches Unternehmen verändert seinen ROA von Quartal zu Quartal um ±1,7 Prozentpunkte (σ Median = 0,017). 43% dieser Veränderung werden im Folgequartal korrigiert."
- ROA-Quadranten-Scatter (bereits als Grafik vorhanden) einbinden und interpretieren
- Sektorale Spreizung: Communication Services (φ₁ = −0,49) vs. Basic Materials (φ₁ = −0,37) — Spanne von 0,12 ökonomisch erklären

Daten: output/ar/ar_summary_by_ratio.csv + FF1_Interpretation_AR1_Diffs.md Abschnitt 3.1

**5.2.2 ROE — Leverage-Verstärkung (~0,75 Seiten)**

Kernunterschied zu ROA: Höhere Änderungsvolatilität (σ Median = 0,048 vs. 0,017) durch Leverage-Hebel. Mean-Median-Divergenz bei σ (0,079 vs. 0,048) zeigt Teilgruppe mit extrem volatiler ROE.

→ Vorgriff auf FF2: Die ROE×D/E-Volatilitätskopplung (ρ = 0,82) hat hier ihren Ursprung. Nissim & Penman (2001) DuPont-Zerlegung als Erklärung.

**5.2.3 EBIT-Marge — Operative Margendynamik (~0,5 Seiten)**

Ähnliche Mean-Reversion wie ROA/ROE, aber viel breitere σ-Spanne (p5 = 0,022 bis p95 = 0,609). Energieunternehmen (σ = 0,259) vs. Consumer Defensive (σ = 0,055) — Faktor 5. Rohstoffpreise vs. stabile Nachfrage.

**5.2.4 FCF-Marge — Stärkste Mean-Reversion (~0,75 Seiten)**

Stärkste Mean-Reversion (φ₁ = −0,46), höchste Signifikanzrate (97%), bester R² (0,21). Warum? Investitions-Bunching-Effekte: Ein Quartal mit hohen Capex wird von einem mit niedrigerem Capex gefolgt.

Vergleich zu EBIT-Marge: σ-Korrelation ist hoch (ρ = 0,78), aber φ₁-Korrelation ist schwach (ρ = 0,15). → FCF und EBIT schwanken zwar zusammen, aber die Autokorrelationsstruktur ist verschieden. Dechow (1994): Accrual-Timing erklärt die Divergenz.

**5.2.5 Current Ratio — Die Übergangszone (~0,5 Seiten)**

Schwerpunkt auf: Warum ist die Mean-Reversion so viel schwächer? Real Estate als Anomalie (φ₁ = −0,34, 82% signifikant vs. −0,17 und 46% gesamt). Erklärung: REIT-Ausschüttungspflichten und regelmäßige Refinanzierungen.

**5.2.6 Kapitalstruktur (D/E + EK-Quote zusammen) (~0,75 Seiten)**

Kein separater Unterabschnitt pro Kennzahl nötig — das Signal ist bei beiden gleich: kein AR-Signal auf Differenzen. Stattdessen:
- Warum auf Differenzen kein Signal, aber auf Levels hohe Persistenz (0,87–0,93)?
- Utilities als einziger Sektor mit substanzieller Kapitalstruktur-Mean-Reversion (φ₁_D/E = −0,17) — regulatorisch erklärbar
- D/E hat bei >25% der Unternehmen positives φ₁ → Persistenz der Veränderungen (Momentum)

---

### 5.3 Robustheit (~3–4 Seiten)

**Aufbau:** Drei Robustheitsdimensionen, jeweils mit Ergebnistabelle und Interpretation.

**5.3.1 Modellvarianten (Levels, AR(2), Δ₄Y) (~1,5 Seiten)**

Kurze Methodik-Erinnerung: Vier Spezifikationen testen dieselbe Hierarchie.

Ergebnistabelle (bereits vorhanden im Anhang — übernehmen und erweitern):

| Kennzahl | diff1 (ΔY) | levels (Y) | AR(2) φ₁ | diff4 (Δ₄Y) |
|----------|:---:|:---:|:---:|:---:|
| ROA | −0,43 | +0,36 | −0,56 | +0,21 |
| ROE | −0,43 | +0,36 | −0,55 | +0,21 |
| EBIT-Marge | −0,43 | +0,57 | −0,55 | +0,30 |
| FCF-Marge | −0,46 | +0,10 | −0,60 | +0,12 |
| Current Ratio | −0,17 | +0,80 | −0,21 | +0,59 |
| Debt/Equity | −0,09 | +0,87 | −0,10 | +0,66 |
| EK-Quote | −0,04 | +0,93 | −0,04 | +0,72 |

Pro Variante 1 Absatz Interpretation:

**Levels:** Hierarchie bestätigt sich spiegelbildlich. Profitabilität hat niedrige Niveau-Persistenz (φ₁ = 0,10–0,36), Kapitalstruktur sehr hohe (0,87–0,93). Diejenigen Kennzahlen, die auf Differenzen kein Signal zeigen (19–46% Signifikanz), sind auf Niveaus hochsignifikant (98–100%).

**AR(2):** Zweiter Lag bringt bei Profitabilität zusätzliche Erklärungskraft (R² steigt von 0,19 auf 0,29). φ₁ wird stärker negativ (−0,55 bis −0,60). Qualitative Aussage bleibt gleich: AR(1) ist konservativer, unterschätzt die Korrekturgeschwindigkeit leicht. Bei Bilanzstruktur ändert sich nichts.

→ Erklärung für den Leser: "Ein zusätzlicher Lag bei Profitabilität bedeutet, dass die Korrektur nicht nur auf den Vorquartalswert reagiert, sondern auch auf die Veränderung zwei Quartale zurück. Das ist konsistent mit mehrstufigen operativen Anpassungsprozessen."

**Δ₄Y:** Vorzeichenwechsel zu positivem φ₁ bei Profitabilität (+0,10 bis +0,21). Jahresveränderungen sind persistent — ein Unternehmen, das sich im Vorjahresvergleich verbessert hat, verbessert sich tendenziell weiter. Aber: Rangordnung bleibt gleich (FCF > ROA ≈ ROE ≈ EBIT > CR > D/E > EQ).

**Kernaussage:** Die Drei-Schichten-Hierarchie ist modellunabhängig. Sie erscheint unter vier verschiedenen Spezifikationen mit jeweils angepasster Interpretation.

**5.3.2 Stichprobenrobustheit (~1 Seite)**

Ergebnistabelle:
| Kennzahl | 100Q (932) | 80Q (1.231) | 60Q (1.855) | 40Q (2.356) | Max. Δ |
|----------|:---:|:---:|:---:|:---:|:---:|
| ROA | −0,432 | −0,429 | −0,433 | −0,432 | 0,4% |
| FCF-Marge | −0,459 | −0,460 | −0,459 | −0,455 | 0,9% |
| Current Ratio | −0,174 | −0,174 | −0,172 | −0,174 | 1,1% |
| D/E | −0,089 | −0,089 | −0,104 | −0,104 | 16,2% |
| EK-Quote | −0,040 | −0,041 | −0,053 | −0,056 | 40,2% |

Interpretation: Profitabilität und Liquidität extrem stabil (<3% Abweichung). Der 100Q-Filter verzerrt die Kernbefunde nicht. Bilanzstruktur weicht bei erweiterten Stichproben ab → jüngere/kurzlebigere Unternehmen haben dynamischere Kapitalstrukturen. Das ist plausibel und muss als Limitation benannt werden.

**5.3.3 Mechanische Abhängigkeit φ₁ × σ (~0,5 Seiten)**

Kurzfassung aus METHODIK_DISKUSSION.md Abschnitt 1: Empirische Korrelation |ρ| < 0,19 für Profitabilität, Monte-Carlo-Benchmark bei ρ = −0,75. Quadranten sind trennbar.

---

### 5.4 Sektorale Heterogenität (~3 Seiten)

**Aufbau:** Nicht 10 gleichlange Sektorabschnitte (das wäre ermüdend), sondern thematisch organisiert.

**5.4.1 Heatmap-Überblick (~0,5 Seiten)**
Heatmap Sektor × Kennzahl (bereits vorhanden im Anhang) einbinden. Leser durch die Muster führen: linke Hälfte (Profitabilität) ist dunkelrot, rechte Hälfte (Bilanzstruktur) ist hellrot. Innerhalb der Profitabilität gibt es eine Spreizung von −0,37 (Basic Materials) bis −0,49 (Communication Services).

**5.4.2 Drei Sektorgruppen nach Dynamik-Profil (~1,5 Seiten)**

Statt 10 Sektoren einzeln → drei Gruppen:

**Gruppe A — Korrektiv-volatile Sektoren (Comm. Services, Energy, Real Estate):**
Gemeinsam: Starke Mean-Reversion + hohe Volatilität. Korrektiv-Volatil als dominanter Quadrant (38–44%).
- Communication Services: Stärkste Profitabilitäts-Mean-Reversion (φ₁ = −0,49). Hohe Fixkosten → Umsatzschwankungen schlagen direkt durch, normalisieren sich aber schnell.
- Energy: Rohstoffpreise treiben σ, aber Mean-Reversion ist durchschnittlich (φ₁ ≈ −0,43).
- Real Estate: Anomalie bei Current Ratio (φ₁ = −0,34 vs. −0,17 gesamt). REIT-Geschäftsmodell.

**Gruppe B — Persistent-volatile Sektoren (Technology, Basic Materials):**
Gemeinsam: Schwächere Mean-Reversion + hohe Volatilität. Persistent-Volatil als stärkster Quadrant (31–32%).
- Technology: Current Ratio mit schwächster Mean-Reversion aller Sektoren (φ₁ = −0,10). Akquisitionsgetriebene Liquiditätschwankungen.
- Basic Materials: Schwächste Profitabilitäts-Mean-Reversion (φ₁ = −0,37). Rohstoffpreiszyklen treiben Profitabilität über mehrere Quartale in eine Richtung.

→ Investorenrelevanz: Diese Sektoren sind am schwierigsten vorhersagbar.

**Gruppe C — Stabile Sektoren (Consumer Defensive, Industrials, Utilities):**
Gemeinsam: Stabile Quadranten dominieren (>60%).
- Consumer Defensive: Niedrigste σ über fast alle Kennzahlen. Stabile Nachfrage.
- Utilities: Sonderrolle bei Kapitalstruktur — einziger Sektor mit substanzieller D/E-Mean-Reversion (φ₁ = −0,17). Regulatorisch bedingt.

**5.4.3 Quadrantenverteilung pro Sektor (~1 Seite)**
Balkendiagramm (bereits vorhanden im Anhang) einbinden. Beschreibung der Muster — welcher Quadrant dominiert wo.

Datenpunkte aus dem Anhang:
- Communication Services: Korrektiv-Volatil dominiert (~49%)
- Basic Materials: Persistent-Volatil dominiert (~31%)
- Consumer Defensive: Stabile Quadranten dominieren (~65%)

---

### 5.5 Zusammenfassung FF1 (~0,5 Seiten)

Drei Kernaussagen:
1. **Kennzahl-Hierarchie:** FCF-Marge > ROA ≈ ROE ≈ EBIT-Marge > Current Ratio > D/E > EK-Quote
2. **Modellrobustheit:** Vier AR-Varianten, vier Stichprobengrößen — Hierarchie stabil
3. **Sektorale Differenzierung:** Innerhalb der Schichten variiert φ₁ um ~0,12 und σ um Faktor 5–10

→ Überleitung zu FF2: "Die Drei-Schichten-Hierarchie beschreibt die *individuelle* Dynamik jeder Kennzahl. FF2 fragt nun: Wie hängen diese Dynamiken *zwischen* Kennzahlen zusammen?"

### To-Do für Kapitel 5

- [ ] ROA-Quadranten-Scatter als Hauptgrafik einbinden (vorhanden als ff1_roa_quadrant_methodik.png)
- [ ] Boxplot-Grafik einbinden (vorhanden im Anhang)
- [ ] Heatmap einbinden (vorhanden im Anhang)
- [ ] Quadrantenverteilung-Balkendiagramm einbinden (vorhanden im Anhang)
- [ ] Dichev & Tang Benchmark-Vergleich konkret durchführen (S. 162–167)
- [ ] Entscheiden: Tabellen im Fließtext oder im Anhang? (Empfehlung: Zusammenfassungstabellen im Text, Detailtabellen im Anhang)
- [ ] Sektortabelle mit φ₁ × σ (10 Sektoren × 7 Kennzahlen) als Anhang-Tabelle vorbereiten

---

# KAPITEL 6: FF2 — Interdependenzen und zeitliche Manifestation

## 6.0 Strukturprinzip

**Umfang:** 8–10 Seiten
**Ziel:** Zeigen, dass die Drei-Schichten-Hierarchie aus FF1 nicht nur eine Rangordnung ist, sondern tatsächlich *separable Dimensionen* der Unternehmensdynamik reflektiert — und dass die Quadrantenklassifikation prädiktive Kraft für Krisenreaktionen hat.

**Verbindung zu Kap. 1–4 und Kap. 5:**
- Kap. 2.1 hat die DuPont-Zerlegung eingeführt → Kap. 6 zeigt die ROE×D/E-Kopplung als mechanische Konsequenz
- Kap. 5.1 hat die Drei-Schichten-Hierarchie etabliert → Kap. 6.1 bestätigt sie auf einer neuen Ebene (Korrelationsstruktur)
- Kap. 4.5 hat die FF2-Methoden vorgestellt → Kap. 6 wendet sie an

**FF2 besteht aus zwei konzeptionell verschiedenen Teilen:**
- Teil A (querschnittlich): Hängen die Dynamikmuster verschiedener Kennzahlen zusammen?
- Teil B (zeitlich): Wie manifestieren sich die Muster in Stressphasen?

Das ist eine natürliche Zweiteilung, die sich auch in der Kapitelstruktur widerspiegeln sollte.

---

### 6.1 FF2-spezifische Methodik (~1 Seite)

**Kurzer Methodik-Einschub** (hybrides Modell aus Kap. 4):

**Querschnittsanalyse:**
- Spearman-Rangkorrelation der φ₁-Werte zwischen Kennzahlenpaaren (21 Paare)
- Spearman-Rangkorrelation der σ(ΔY)-Werte zwischen Kennzahlenpaaren
- Cramér's V für Quadrantenüberschneidungen (χ²-Tests auf 4×4-Kontingenztafeln)

**Zeitliche Analyse:**
- Datengetriebene Peak-Identifikation: Quartal gilt als "Peak-Window" wenn ≥3 der 7 Kennzahlen gleichzeitig das 90. Perzentil der rollierenden Querschnittsvolatilität überschreiten
- Kein ex-ante-Datum (z.B. "Lehman = 2008Q3"), sondern rein aus den Finanzkennzahlen abgeleitet
- Non-parametrische Tests: Mann-Whitney U (Paarvergleiche), Kruskal-Wallis (Gesamtvergleich), Bonferroni-Korrektur

→ Warum non-parametrisch? Weil die ΔY-Verteilungen in Events nicht normalverteilt sind (starke Schiefe durch Outlier-Reaktionen).

---

### 6.2 Querschnittliche Interdependenz der φ₁-Werte (~2 Seiten)

**A) Die φ₁-Korrelationsmatrix:**

Exakte Daten aus corr_phi1.csv:

| | ROA | ROE | EBIT | FCF | CR | D/E | EQ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ROA | 1,00 | **0,78** | **0,54** | 0,20 | 0,08 | 0,08 | 0,07 |
| ROE | | 1,00 | **0,50** | 0,16 | 0,07 | 0,07 | 0,09 |
| EBIT | | | 1,00 | 0,15 | 0,05 | 0,05 | 0,07 |
| FCF | | | | 1,00 | 0,08 | 0,02 | 0,09 |
| CR | | | | | 1,00 | 0,10 | **0,22** |
| D/E | | | | | | 1,00 | **0,26** |
| EQ | | | | | | | 1,00 |

**Drei Befunde herausarbeiten:**

**Befund 1 — Blockstruktur:** Profitabilitätsschicht intern stark korreliert (ROA×ROE = 0,78; ROA×EBIT = 0,54; ROE×EBIT = 0,50). Ein Unternehmen mit starker ROA-Mean-Reversion zeigt mit hoher Wahrscheinlichkeit auch starke ROE- und EBIT-Margen-Mean-Reversion. → Bestätigt FF1-Hierarchie auf neuer Ebene.

**Befund 2 — Schichtübergreifende Unabhängigkeit:** Alle cross-kategorialen Korrelationen < 0,10. Die Dynamik der Profitabilität sagt nichts über die Dynamik der Bilanzstruktur aus. → Die Schichten messen tatsächlich verschiedene Dimensionen.

**Befund 3 — FCF als Sonderfall:** FCF korreliert schwächer mit ROA/ROE/EBIT (ρ = 0,15–0,20) als die drei untereinander. Cashflow-basierte und buchhalterische Kennzahlen haben ähnliche Mean-Reversion-Stärke, aber die *Dynamik-Profile* sind weniger gekoppelt. → Dechow (1994): Accrual-Timing erzeugt eine Entkopplung der Autokorrelationsstrukturen.

**B) Vergleich mit σ-Korrelationsmatrix:**

Exakte Daten aus corr_sigma.csv — das Muster ist ANDERS als bei φ₁:

Hervorheben: ROE×D/E σ-Korrelation = **0,82** (stärkster Wert überhaupt). Bei φ₁ nur 0,07. → DuPont-Mechanik: ROE = Gewinn/EK. Wenn EK schwankt (hohe D/E-Volatilität), schwankt ROE automatisch mit — unabhängig von der operativen Performance.

EBIT×FCF σ-Korrelation = **0,78** (hohe Kovarianz der Volatilität), aber φ₁-Korrelation nur 0,15. → Unternehmen mit volatilen Margen haben volatile Cashflows, aber die Autokorrelationsstruktur (wie schnell korrigiert?) ist entkoppelt.

EQ-Quote als "Brücke": σ-Korrelation mit ROA = 0,57, mit CR = 0,34, mit D/E = 0,29. Einzige Kennzahl, die über alle Schichten hinweg Volatilitätszusammenhänge zeigt.

**C) Cramér's V — Quadrantenüberschneidungen:**

Exakte Daten aus quadrant_crosstabs.csv:

| Paar | Cramér's V | Interpretation |
|------|:---:|---|
| ROA × ROE | 0,60 | Sehr starke Quadranten-Übereinstimmung |
| ROA × EBIT | 0,31 | Moderate Übereinstimmung |
| ROE × EBIT | 0,29 | Moderate Übereinstimmung |
| EBIT × FCF | 0,28 | Moderate Übereinstimmung |
| ROE × D/E | 0,27 | Leverage-getrieben (σ-Kopplung) |
| D/E × EQ | 0,25 | Bilanzstruktur-Cluster |
| ROE × FCF | 0,09 | Nicht relevant |

Alle 21 Paare signifikant (p < 0,05). Effektstärken bestätigen Blockstruktur.

---

### 6.3 Zeitliche Manifestation: Event-Analyse (~3–4 Seiten)

**6.3.1 Identifizierte Peak-Windows (~0,5 Seiten)**

Methode: ≥3 Kennzahlen über 90. Perzentil rollierender Querschnittsvolatilität.

Ergebnis: Drei Events — Dot-Com 2001Q4, GFC 2009Q2, COVID 2020Q3.

Wichtig betonen: Die Events wurden *nicht* ex-ante definiert, sondern rein aus den Finanzkennzahlen identifiziert. Dass sie mit bekannten Krisen korrespondieren, validiert die Methode.

COVID (2020Q3) als breitester Peak: 6 von 7 Kennzahlen gleichzeitig betroffen. GFC (2009Q2): 5 von 7. Dot-Com (2001Q4): ≥3, primär Profitabilität.

**6.3.2 Quadranten-Reaktionen auf Events (~1,5 Seiten)**

Kernfrage: Reagieren KORREKTIV-klassifizierte Unternehmen anders als PERSISTENT-klassifizierte?

Am Beispiel COVID 2020Q3 (ROA):

| Quadrant | Median ΔY | σ(ΔY) |
|----------|:---------:|:-----:|
| Korrektiv-Stabil | +0,0004 | 0,014 |
| Persistent-Stabil | +0,0013 | 0,014 |
| Korrektiv-Volatil | +0,0026 | 0,036 |
| Persistent-Volatil | +0,0034 | 0,035 |

**Interpretation (das ist der interpretative Teil, den Stollhoff einfordert):**

Die Differenz zwischen Korrektiv-Stabil und Persistent-Volatil beträgt Faktor 8×. Das bedeutet: Die Quadrantenklassifikation, die auf dem gesamten 25-Jahres-Zeitraum geschätzt wurde, hat *prädiktive Kraft* für das Verhalten in einem konkreten Krisenereignis.

Warum reagieren Korrektiv-Volatile stärker? Weil diese Unternehmen generell stärker auf Schocks reagieren — das ist ja gerade die Definition des Quadranten. Der Mehrwert ist, dass die *statische* Klassifikation aus FF1 sich in *dynamischen* Situationen als informativ erweist.

**6.3.3 Sektor-Reaktionsprofile (~1 Seite)**

Pro Event: Welche Sektoren reagieren am stärksten?

**Dot-Com 2001Q4:** Industrials am stärksten negativ betroffen (Median ΔY = −0,00138). Überraschend: Technology nicht negativ — Survivorship Bias ist hier sichtbar (die betroffenen Start-ups sind nicht im 100Q-Sample).

**GFC 2009Q2:** Alle Sektoren positiv (Recovery-Phase). Basic Materials (+0,0037) und Consumer Cyclical (+0,0032) erholen sich am schnellsten — zyklische Sektoren profitieren am stärksten vom Stimulus.

**COVID 2020Q3:** Consumer Cyclical stärkster Rebound (+0,0044) — Nachholeffekt nach Lockdown.

**6.3.4 Quadrant × Sektor Interaktion (~0,5 Seiten)**

Der wichtigste Befund für die Diskussion: Innerhalb eines Sektors differenziert der Quadrant die Reaktion. Korrektiv-Volatile Tech-Unternehmen reagieren in COVID 1,5–2× stärker als Persistent-Stabile Tech-Unternehmen im selben Sektor.

→ Die Quadrantenklassifikation fügt Erklärungskraft *über den Sektoreffekt hinaus* hinzu.

---

### 6.4 Zusammenfassung FF2 (~0,5 Seiten)

Zwei Hauptbefunde:
1. **Schichtinterne Kohärenz, schichtübergreifende Unabhängigkeit:** Die Drei-Schichten-Hierarchie ist nicht nur eine Rangordnung, sondern reflektiert separable Dynamik-Dimensionen.
2. **Prädiktive Kraft der Quadrantenklassifikation:** Die statische Klassifikation aus FF1 manifestiert sich in konkreten Event-Reaktionen.

→ Überleitung zu FF3: "FF2 hat gezeigt, dass die Dynamikmuster intern kohärent und zeitlich informativ sind. FF3 fragt nun: Welche *externen* Merkmale bestimmen, in welchem Quadranten ein Unternehmen landet?"

### To-Do für Kapitel 6

- [ ] Korrelationsmatrizen als Heatmap-Grafiken erstellen (für Arbeit, nicht nur als Tabelle)
- [ ] Event-Reaktions-Tabellen für alle drei Events aufbereiten (nicht nur COVID-Beispiel)
- [ ] Mann-Whitney und Kruskal-Wallis Ergebnisse formal berichten
- [ ] Sektor-Reaktionsprofile als Grafik aufbereiten (Balkendiagramme pro Event)
- [ ] Prüfen: Gibt es eine Quadrant×Sektor-Interaktionsgrafik? Falls nicht, erstellen.

---

# KAPITEL 7: FF3 — Externe Validierung

## 7.0 Strukturprinzip

**Umfang:** 8–10 Seiten
**Ziel:** Zeigen, dass die Quadrantenklassifikation ökonomisch interpretierbar und nicht ein statistisches Artefakt ist — indem sie mit externen Merkmalen (Branche, Größe) verknüpft wird.

**Verbindung zu Kap. 1–4, 5, 6:**
- Kap. 3.2 hat den Fama-French-Größeneffekt eingeführt → Kap. 7.3 testet ihn empirisch
- Kap. 5.4 hat sektorale Heterogenität gezeigt → Kap. 7.2 quantifiziert den Sektoreffekt
- Kap. 6.2 hat die Blockstruktur gezeigt → Kap. 7.1 zeigt, dass die Konsistenz schichtbasiert ist

**Stollhoffs Feedback adressieren:**
- "Median-Split als Schwäche" → K-Means-Robustheitscheck (7.4) zeigt, dass die Hauptdifferenzierung bestätigt wird
- "Mehr Interpretation" → Geschäftsmodell-Bezüge (warum Healthcare im volatilen Cluster überrepräsentiert ist etc.)

---

### 7.1 Das "Was ist das Unternehmen?"-Problem (~1,5 Seiten)

**Ausgangsproblem:** Ein Unternehmen hat 7 Quadrantenzuordnungen (eine pro Kennzahl). Apple kann für ROA Korrektiv-Stabil sein, für Current Ratio aber Persistent-Volatil. Gibt es überhaupt ein einheitliches Unternehmensprofil?

**Konsistenz-Scores (exakte Daten aus consistency_summary.csv):**

| Ebene | Mean | Median | Voll konsistent | Mehrheit (≥50%) |
|-------|:----:|:------:|:---------------:|:---------------:|
| Gesamt (7 Ratios) | 0,557 | 0,571 | 1,2% | 59,0% |
| Profitabilität (4 Ratios) | 0,666 | 0,750 | 15,6% | 97,6% |
| Kapitalstruktur (2 Ratios) | 0,708 | 0,500 | 41,5% | 100% |

**Drei Schlussfolgerungen:**
1. Quadranten sind primär *ratio-spezifisch*, nicht unternehmensspezifisch (nur 1,2% voll konsistent)
2. Aber: Innerhalb der Profitabilitätsschicht haben 97,6% ein konsistentes Mehrheitsprofil → schichtbasierte Klassifikation ist sinnvoll
3. Das bestätigt FF2: Schichtinterne Kohärenz, schichtübergreifende Unabhängigkeit — jetzt aus der Unternehmensperspektive

**Dominante Quadranten:**
Persistent-Stabil (30,2%) > Korrektiv-Volatil (27,3%) > Korrektiv-Stabil (21,7%) > Persistent-Volatil (20,9%). Annähernd gleichverteilt, leichte Überrepräsentation stabiler Profile.

→ Verbindung zu 2.4: Der Median-Split erzeugt keine extreme Schieflage — die Quadranten sind ähnlich groß.

---

### 7.2 Brancheneffekte: χ²-Tests (~2 Seiten)

**FF3-spezifische Methodik (kurz):**
χ²-Tests auf Unabhängigkeit: Sektor × Quadrant für jede der 7 Kennzahlen.

**Ergebnistabelle (exakte Daten aus ff3_chi2_results.csv):**

| Kennzahl | χ² | p | Cramér's V | n |
|----------|:---:|:---:|:---:|:---:|
| Current Ratio | 226,8 | <0,001 | **0,286** | 925 |
| EBIT-Marge | 221,2 | <0,001 | **0,282** | 925 |
| FCF-Marge | 201,9 | <0,001 | **0,270** | 925 |
| ROA | 170,4 | <0,001 | **0,248** | 924 |
| EK-Quote | 136,2 | <0,001 | **0,222** | 925 |
| ROE | 93,5 | <0,001 | **0,184** | 924 |
| D/E | 85,8 | <0,001 | **0,176** | 924 |

**Interpretation:**

Alle 7 Tests hochsignifikant. Cramér's V = 0,18–0,29 → kleine bis mittlere Effektstärke.

Die stärksten Brancheneffekte bei Current Ratio (V = 0,286) und EBIT-Marge (V = 0,282). Ökonomisch plausibel: Liquiditätsmanagement und operative Margenstruktur sind stark branchenabhängig (vgl. Real Estate CR φ₁ = −0,34 vs. Technology CR φ₁ = −0,10 aus Kap. 5).

Die schwächsten Effekte bei D/E (V = 0,176) und ROE (V = 0,184). Verschuldungsentscheidungen werden stärker durch unternehmensspezifische Faktoren als durch Branchenzugehörigkeit bestimmt.

**Kernargument für die Arbeit:** Moderate V-Werte (0,18–0,29) zeigen: Branche erklärt einen Teil, aber nicht alles. Die Quadrantenklassifikation fängt unternehmensspezifische Dynamik-Merkmale ein, die *über* den Brancheneffekt hinausgehen. → Wäre V ≈ 1, wäre die Klassifikation redundant zur Branchenklassifikation.

**Zusätzlich: Kruskal-Wallis-Tests (aus ff3_summary.md):**
Direkte Tests Sektor → φ₁ und Sektor → σ(ΔY). η²-Werte für σ (0,05–0,22) deutlich höher als für φ₁ (0,02–0,07). → Branche erklärt die Volatilitätsdimension stärker als die Persistenzdimension. Das ist konsistent mit den Größeneffekten (7.3).

---

### 7.3 Größeneffekte (~2 Seiten)

**Exakte Daten aus ff3_size_effects.csv:**

**Haupttabelle — die stärksten Zusammenhänge:**

| Kennzahl | Größe | vs. φ₁ (ρ) | sig? | vs. σ(ΔY) (ρ) | sig? |
|----------|-------|:---:|:---:|:---:|:---:|
| FCF-Marge | Employees | −0,09 | ✓ | **−0,53** | ✓ |
| Current Ratio | Employees | +0,09 | ✓ | **−0,53** | ✓ |
| EBIT-Marge | Employees | −0,04 | ✗ | **−0,41** | ✓ |
| EK-Quote | Employees | +0,08 | ✓ | **−0,27** | ✓ |
| ROA | Employees | −0,03 | ✗ | **−0,19** | ✓ |
| ROA | MarketCap | −0,04 | ✗ | **−0,21** | ✓ |

**Drei Befunde:**

**Befund 1 — Volatilität ist größenabhängig, Persistenz nicht:**
Die stärksten Korrelationen sind Employees × σ(ΔY) bei FCF-Marge (ρ = −0,53) und Current Ratio (ρ = −0,53). Kein einziger MarketCap × φ₁ Zusammenhang ist signifikant. → Die zwei Achsen des Quadrantenframeworks haben *unterschiedliche externe Treiber*.

**Befund 2 — Employees > MarketCap:**
Operationale Größe (Mitarbeiter) ist ein besserer Prädiktor als finanzielle Größe (Marktkapitalisierung). Mehr Mitarbeiter = mehr Standorte/Produkte/Kunden = mehr Diversifikation = weniger volatile Kennzahlen. → Konsistent mit Diversifikationshypothese.

Fama & French (1992) Vergleich: Sie zeigen Größeneffekte auf Renditen. Du erweiterst das: Größe wirkt auf die *Dynamik* der Kennzahlen — und zwar nur auf die Volatilitätsdimension.

**Befund 3 — D/E als Ausnahme:**
Debt-to-Equity zeigt keinerlei Größeneffekt (weder φ₁ noch σ). Die dynamischste Kennzahl in der Bilanzstrukturschicht ist zugleich die am stärksten unternehmensspezifische — weder Branche noch Größe erklären die Verschuldungsdynamik.

---

### 7.4 K-Means als Robustheitscheck (~1,5 Seiten)

**Methodik:** K-Means auf AR-Dynamik-Features (φ₁ und σ pro Ratio, k=2).

**Ergebnis:**
| | Cluster 0 (n=751, 81%) | Cluster 1 (n=180, 19%) |
|---|:---:|:---:|
| ROA φ₁ / σ | −0,434 / 0,014 | −0,426 / 0,033 |
| D/E φ₁ / σ | −0,067 / 0,140 | **−0,214 / 2,605** |
| Employees Median | 10.616 | 5.050 |

**Interpretation:**
Cluster 0 = "Stabile Mehrheit". Cluster 1 = "Hochvolatile Minderheit" mit 2–3× höherer σ, aber ähnlichem φ₁. → Die Hauptdifferenzierung läuft über die *Volatilitätsachse*, nicht über Persistenz. Das ist konsistent mit den Größeneffekten (σ ist größenabhängig, φ₁ nicht).

Sektorale Zusammensetzung: Healthcare (37%) und Energy (31%) überrepräsentiert in Cluster 1. Industrials (11%) und Utilities (10%) unterrepräsentiert. → Konsistent mit den Sektorprofilen aus Kap. 5.4.

**Warum bestätigt K-Means den Median-Split?** Weil beide Ansätze zur selben Hauptaussage kommen: Die Volatilitätsdimension ist der stärkste Differenzierer. Der Median-Split macht das über zwei separate Achsen transparent, K-Means fasst sie multivariat zusammen. Die qualitative Aussage ist identisch.

→ Adressiert Stollhoffs Kritik am Median-Split: "Ja, der Median-Split ist einfach und willkürlich. Aber K-Means als datengetriebener Ansatz bestätigt die Kerndifferenzierung."

---

### 7.5 Financial Services: Regulatorische Mean-Reversion (~1 Seite)

Exklusion des Finanzsektors in der Hauptanalyse, aber separate Analyse als Robustheitscheck.

| Kennzahl | Hauptanalyse (932) | FinServ 100Q (176) | Δ |
|----------|:---:|:---:|---|
| ROA | −0,43 | −0,43 | Identisch |
| Current Ratio | −0,17 | **−0,41** | Massiver Unterschied |
| D/E | −0,09 | **−0,20** | Starker Unterschied |

Interpretation: Im Finanzsektor verschmilzt die Liquiditätsschicht mit der Profitabilitätsschicht. Basel III / Solvency II erzeugen regulatorische Mean-Reversion bei Bilanz- und Liquiditätskennzahlen, die bei unregulierten Unternehmen fehlt. Die Profitabilitätsdynamik ist sektorunabhängig (φ₁ identisch).

→ Rechtfertigt die Exklusion: Finanzsektor hat systematisch andere Bilanz-Dynamiken. Separate Behandlung im Anhang.

---

### 7.6 Zusammenfassung FF3 (~0,5 Seiten)

Vier Hauptbefunde:
1. Die Quadrantenklassifikation ist *ökonomisch interpretierbar* (χ² p < 0,001, V = 0,18–0,29)
2. Die zwei Dimensionen (φ₁, σ) haben *unterschiedliche externe Treiber* (σ ← Größe, φ₁ ← nicht)
3. K-Means bestätigt die Hauptdifferenzierung über die Volatilitätsachse
4. Der Finanzsektor zeigt regulatorische Mean-Reversion — Exklusion gerechtfertigt

→ Überleitung zu Kap. 8: "Die Kapitel 5–7 haben FF1–FF3 empirisch beantwortet. Kapitel 8 diskutiert die Implikationen, Limitationen und die Einordnung in den Forschungsstand."

### To-Do für Kapitel 7

- [ ] χ²-Ergebnistabelle formatieren (fertig aufbereitet)
- [ ] Größeneffekte als Scatter-Plots visualisieren (Employees × σ für FCF-Marge wäre eindrucksvoll)
- [ ] K-Means Cluster als Profil-Scatter mit Farb-Overlay darstellen
- [ ] Financial Services Vergleichstabelle aufbereiten
- [ ] Prüfen: Braucht es eine separate Konsistenz-Grafik für das "Was ist das Unternehmen?"-Problem?

---

# KAPITEL 8: Diskussion

## 8.0 Strukturprinzip

**Umfang:** 6–8 Seiten
**Ziel:** Die Ergebnisse interpretieren, in die Literatur einordnen, Limitationen transparent benennen, und praktische Implikationen aufzeigen. Dies ist das Kapitel, das die Arbeit von einer reinen Datenanalyse zu einem wissenschaftlichen Beitrag macht.

**Stollhoffs Feedback direkt adressieren:**
- "Mehr Interpretation, z.B. Geschäftsmodell-Zusammenhang" → Abschnitt 8.1
- "Diskussion der Schwächen, z.B. Median-Split" → Abschnitt 8.3
- "Literatureinbettung" → Abschnitt 8.2

---

### 8.1 Ökonomische Interpretation der Befunde (~2 Seiten)

**Hier geht es um das WARUM — nicht das WAS.**

**A) Warum die Drei-Schichten-Hierarchie?**

Die Hierarchie spiegelt den *Grad der Marktexposition* wider:
- Profitabilitätskennzahlen sind Output-Kennzahlen — sie aggregieren Marktbedingungen (Nachfrage, Wettbewerb, Preise). Quartalsveränderungen enthalten temporäre Komponenten, die sich zurückbilden.
- Kapitalstruktur-Kennzahlen sind Input-Kennzahlen — sie reflektieren Managemententscheidungen (Finanzierungsmix). Veränderungen sind diskret und intentional, nicht mean-revertierend.
- Liquidität ist hybrid: teilweise operativ (Zahlungsströme), teilweise gesteuert (Kreditlinien).

**B) Geschäftsmodell-Zusammenhang in den Sektoren:**

Hier die inhaltliche Brücke, die Stollhoff einfordert — nicht "Communication Services hat φ₁ = −0,49", sondern *warum*:

- **Communication Services** (höchste Mean-Reversion): Hohe Fixkostenstruktur (Netzwerkinfrastruktur, Lizenzen). Umsatzschwankungen schlagen voll auf die Marge durch, aber die Kostenstruktur normalisiert sich schnell. Ein Blockbuster-Quartal (z.B. Streaming-Launch) ist einmalig.

- **Basic Materials** (niedrigste Mean-Reversion): Rohstoffpreiszyklen. Wenn Kupferpreise steigen, profitiert ein Minenbetreiber über mehrere Quartale — die Veränderung ist weniger temporär.

- **Utilities** (Kapitalstruktur-Anomalie): Regulatorische Eigenkapitalanforderungen erzeugen einen "Zielwert", zu dem die Verschuldung systematisch zurückkehrt. Ohne Regulierung fehlt dieser Mechanismus.

- **Technology** (persistent-volatil): Akquisitionsgetriebene Wachstumsmodelle. Große, diskontinuierliche Veränderungen (M&A), die nicht korrigiert werden, sondern das neue Normal definieren.

**C) Die zwei Dimensionen als unterschiedliche Konstrukte:**

φ₁ misst die *Struktur* des Geschäftsmodells (wie temporär sind Veränderungen?).
σ misst die *Exposition* gegenüber externen Schocks (wie stark schwankt die Kennzahl?).

Dass Größe nur σ beeinflusst und nicht φ₁ hat eine elegante Implikation: Diversifikation glättet die Amplituden, aber nicht die Korrekturgeschwindigkeit. Ein großes und ein kleines Unternehmen im selben Sektor korrigieren gleich schnell, aber das kleine schwankt stärker.

---

### 8.2 Einordnung in die Literatur (~2 Seiten)

**A) Dichev & Tang (2009) — Bestätigung und Erweiterung:**
Ihre Befunde zur Earnings-Persistenz werden bestätigt (vergleichbare φ₁-Werte). Erweiterung: Du zeigst, dass der Effekt nicht auf Earnings beschränkt ist, sondern eine systematische Hierarchie über 7 Kennzahlentypen bildet.

**B) Fairfield & Yohn (2001) — Differenzen informativer als Niveaus:**
Ihre These wird empirisch gestützt: Erste Differenzen offenbaren die Drei-Schichten-Hierarchie direkt, während Niveaus die spiegelbildliche (aber interpretatorisch kompliziertere) Perspektive liefern.

**C) Fama & French (1992) — Größeneffekt neu interpretiert:**
Ihr Size-Faktor wirkt auf Renditen. Dein Befund erweitert: Größe wirkt auf die Dynamik der *Kennzahlen selbst* — und zwar nur auf die Volatilitätsdimension.

**D) Dechow (1994) — Accrual-Cashflow-Divergenz:**
Die schwache φ₁-Korrelation zwischen EBIT-Marge und FCF-Marge (ρ = 0,15) trotz hoher σ-Korrelation (ρ = 0,78) ist ein direkter Beleg für Dechows Argument: Buchhalterische Glättung (Accruals) verändert die Autokorrelationsstruktur.

**E) Abgrenzung zu nicht verwendeten Methoden:**
- VAR (Love & Zicchino 2006): Cross-kategoriale φ₁-Korrelationen < 0,10 → wenig dynamische Kausalität zwischen Schichten → VAR-Ansatz nicht informativ
- GARCH: Deine Frage ist die Autokorrelation der Mittelwerte, nicht die bedingte Varianz

---

### 8.3 Limitationen (~2 Seiten)

**Transparent und ehrlich — das zeigt wissenschaftliche Reife.**

**A) Median-Split:**
Willkürliche Grenzziehung. Unternehmen nahe dem Median könnten in beiden Quadranten landen. Milderung: K-Means bestätigt die Hauptdifferenzierung. Alternative: Tercile oder Quartile — aber verliert Interpretierbarkeit.

**B) Survivorship Bias:**
100Q-Filter exkludiert 77% der Ticker. Die verbleibenden 932 sind "Überlebende". Milderung: Variable Stichproben (80Q–40Q) zeigen < 3% Abweichung bei Profitabilität. Bilanzstruktur weicht stärker ab (bis 40%) → Limitation für Kapitalstruktur-Befunde.

**C) Stationaritätsannahme:**
Erste Differenzen stellen Stationarität sicher, aber: Haben sich die Dynamikmuster über 25 Jahre verändert? Rolling-AR-Analyse wäre eine sinnvolle Erweiterung (erwähnen als Ausblick).

**D) Einheitliche Transformation:**
Alle 7 Kennzahlen mit derselben Methode. Für Kapitalstruktur wäre ein Levels-Modell "besser" im Sinne höherer R². Trade-off wurde in Kap. 4 begründet, muss hier als Limitation wiederholt werden.

**E) Kausalität:**
Die Arbeit zeigt Korrelationen und Muster, keine Kausalität. Die Drei-Schichten-Hierarchie ist deskriptiv, nicht kausal begründet. Granger-Kausalität wurde bewusst nicht eingesetzt (begründet in Kap. 6).

**F) US-Fokus:**
Nur S&P 1500 (US-Unternehmen, US-GAAP). Generalisierbarkeit auf IFRS-Berichterstatter, Emerging Markets, kleinere Volkswirtschaften ist nicht gegeben.

---

### 8.4 Praktische Implikationen (~0,5 Seiten)

Kurz halten — die Arbeit ist primär akademisch, aber:
- Für Analysten: Quadrantenklassifikation als Risiko-Screener (Persistent-Volatile Unternehmen zeigen die unvorhersagbarsten Veränderungen)
- Für Portfoliomanagement: Die Drei-Schichten-Hierarchie zeigt, welche Kennzahlen für kurzfristige Prognosen nützlich sind (Profitabilität: ja; Kapitalstruktur: nein)
- Für Kreditanalyse: Financial Services zeigen regulatorische Mean-Reversion bei Bilanzstruktur — anders als nicht-regulierte Unternehmen

### To-Do für Kapitel 8

- [ ] Dichev & Tang Benchmark-Vergleich konkret aufschreiben (exakte Zahlen nebeneinanderstellen)
- [ ] Geschäftsmodell-Erklärungen für mindestens 5 Sektoren ausformulieren
- [ ] Literaturverweise auf alle 10+ Quellen verteilen
- [ ] Rolling-AR-Analyse als Ausblick formulieren (nicht durchführen, nur als Future Work benennen)

---

# KAPITEL 9: Fazit und Ausblick

## 9.0 Strukturprinzip

**Umfang:** 2–3 Seiten
**Ziel:** Die Arbeit abschließen — Kernaussagen komprimieren, Beitrag benennen, Ausblick geben.

---

### 9.1 Zusammenfassung der Ergebnisse (~1 Seite)

Drei Absätze, jeweils einer pro FF:

**FF1:** Die AR(1)-Analyse auf ersten Differenzen identifiziert eine robuste Drei-Schichten-Hierarchie: Profitabilitätskennzahlen (φ₁ ≈ −0,43 bis −0,46) zeigen starke, konsistente Mean-Reversion der Quartalsveränderungen; Liquidität zeigt schwache Mean-Reversion (φ₁ ≈ −0,17); Kapitalstruktur zeigt keine (φ₁ ≈ −0,04 bis −0,09). Diese Hierarchie ist modellübergreifend robust und stichprobenunabhängig.

**FF2:** Die Dynamikmuster sind schichtintern korreliert (ROA×ROE φ₁-Korrelation ρ = 0,78), schichtübergreifend unabhängig (< 0,10). Die Quadrantenklassifikation hat prädiktive Kraft für Event-Reaktionen — Korrektiv-klassifizierte Unternehmen reagieren bis zu 8× stärker als Persistent-Stabile in Krisenquartalen.

**FF3:** Die Quadrantenklassifikation ist ökonomisch interpretierbar: Branche erklärt einen Teil der Zuordnung (Cramér's V = 0,18–0,29), Unternehmensgröße beeinflusst die Volatilitätsdimension (ρ bis −0,53), aber nicht die Persistenz. K-Means bestätigt die Klassifikation multivariat.

---

### 9.2 Wissenschaftlicher Beitrag (~0,5 Seiten)

Was ist NEU an dieser Arbeit?
1. **Systematischer Vergleich:** Erstmals werden 7 Kennzahlen über 3 Kategorien mit derselben Methode verglichen.
2. **Veränderungsperspektive:** Mean-Reversion der Veränderungen statt Persistenz der Niveaus — konzeptionell neu.
3. **Quadrantenklassifikation:** Zweidimensionale Typisierung (φ₁ × σ) mit externer Validierung — existiert so nicht in der Literatur.

---

### 9.3 Ausblick (~0,5–1 Seite)

**Erweiterungsmöglichkeiten (für zukünftige Forschung, NICHT für diese Arbeit):**

1. **Rolling-AR-Analyse:** Haben sich die Dynamikmuster über die 25 Jahre verändert? Rollierende 20Q-Fenster könnten Strukturbrüche identifizieren (z.B. vor/nach GFC).

2. **Internationale Erweiterung:** Gelten die Befunde auch für europäische oder asiatische Märkte? IFRS-Berichterstattung könnte zu anderen Dynamiken führen.

3. **Machine-Learning-Klassifikation:** Statt Median-Split oder K-Means: Random Forest oder Gradient Boosting für die Quadrantenzuordnung, mit Branche/Größe/Sektor als Features.

4. **Granularere Saisonalitätsanalyse:** Q1-zu-Q2 vs. Q3-zu-Q4 — gibt es systematische Unterschiede in der Mean-Reversion-Stärke?

5. **Granger-Kausalität zwischen Schichten:** Auch wenn die Querschnittskorrelationen niedrig sind — zeitliche Kausalität innerhalb einzelner Unternehmen könnte existieren.

### To-Do für Kapitel 9

- [ ] Drei FF-Zusammenfassungen auf je max. 5 Sätze komprimieren
- [ ] Wissenschaftlichen Beitrag scharf formulieren (Abgrenzung zu Dichev & Tang)
- [ ] Ausblick: Nur realistische Erweiterungen benennen, keine Wunschliste

---

# GESAMTÜBERSICHT: Logische Abstimmung

## Roter Faden — Kapitelübergänge

| Von → Nach | Überleitung |
|------------|-------------|
| 1 → 2 | "Die Einleitung hat die Forschungsfragen formuliert. Kapitel 2 legt die theoretischen Grundlagen." |
| 2 → 3 | "Die theoretischen Konzepte sind eingeführt. Kapitel 3 zeigt, was die Literatur bereits weiß — und wo die Lücke ist." |
| 3 → 4 | "Die Forschungslücke ist identifiziert. Kapitel 4 beschreibt das methodische Werkzeug, um sie zu schließen." |
| 4 → 5 | "Die Methodik steht. Kapitel 5 wendet sie an und beantwortet FF1." |
| 5 → 6 | "FF1 hat individuelle Dynamikmuster etabliert. FF2 fragt: Wie hängen sie zusammen?" |
| 6 → 7 | "FF2 hat interne Kohärenz gezeigt. FF3 fragt: Was bestimmt die Zuordnung von außen?" |
| 7 → 8 | "FF1–FF3 sind beantwortet. Kapitel 8 diskutiert die Implikationen und Grenzen." |
| 8 → 9 | "Die Diskussion hat die Befunde eingeordnet. Kapitel 9 fasst zusammen und blickt nach vorne." |

## Stollhoff-Feedback-Checkliste

| Feedback-Punkt | Wo adressiert | Status |
|----------------|---------------|--------|
| Modellgleichungen für Levels, AR(2), Δ₄Y | Kap. 2.3 (Theorie) + Kap. 4.2 (Begründung) + Kap. 5.3 (Anwendung) | ✅ Eingeplant |
| Interpretation / Geschäftsmodell-Bezug | Kap. 5.4 (sektoral) + Kap. 8.1 (Diskussion) | ✅ Eingeplant |
| Diskussion der Schwächen (Median-Split) | Kap. 7.4 (K-Means) + Kap. 8.3 (Limitationen) | ✅ Eingeplant |
| Literatureinbettung | Kap. 3 (systematisch) + Kap. 8.2 (Einordnung) | ✅ Eingeplant |

## Grafiken und ihre Kapitelzuordnung

| Grafik | Quelle | Kapitel |
|--------|--------|---------|
| TAP/QCOM Balkendiagramme (Mean-Reversion-Beispiel) | ff1_meanrev_charts.xlsx / Anhang S.1 | 5.1 oder 4.2 |
| ROA Quadranten-Scatter (10 Unternehmen) | ff1_roa_quadrant_methodik.png / Anhang S.1 | 5.2.1 |
| Boxplots Drei-Schichten-Hierarchie | Anhang S.2 | 5.1 |
| Signifikanz- und R²-Barplots | Anhang S.3 | 5.1 |
| Modellvergleichstabelle | Anhang S.2 | 5.3.1 |
| Heatmap Sektor × Kennzahl | Anhang S.3 | 5.4.1 |
| Quadrantenverteilung pro Sektor | Anhang S.4 | 5.4.3 |
| φ₁-Korrelationsmatrix (Heatmap) | Zu erstellen | 6.2 |
| σ-Korrelationsmatrix (Heatmap) | Zu erstellen | 6.2 |
| Event-Reaktionen (Balkendiagramme) | Zu erstellen | 6.3 |
| χ²-Ergebnistabelle | ff3_chi2_results.csv | 7.2 |
| Größeneffekte (Scatter) | Zu erstellen | 7.3 |
| K-Means Cluster-Overlay | Zu erstellen | 7.4 |

---

*Gliederung vollständig. Nächster Schritt: Schreibbeginn bei Kapitel 4.2 (Modellspezifikation) als Meeting-Vorbereitung.*
