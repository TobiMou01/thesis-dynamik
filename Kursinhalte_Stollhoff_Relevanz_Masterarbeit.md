# Kurs Stollhoff (BM-Fin Quantitative Methoden, WS 23/24) — Relevanz für die Masterarbeit

Stand: 21.05.2026. Synthese auf Basis der vier methodisch zentralen PDFs aus dem Moodle-Kursraum (https://elearning.th-wildau.de/course/view.php?id=19788).

---

## 1. ARIMA Theoretische Grundlagen — kommentiert (44 Seiten)

Konsolidierte Fassung mit Teilen 1–5 in einem Foliensatz. Inhaltlich der zentrale Bezugstext für **Kap. 2.3.1 (AR-Modell)** und **Kap. 3 (Methodik)** der Arbeit.

**Aufbau**:
- S. 2–13: Einführung in stochastische Prozesse (White Noise, Random Walk, Differenzenprozess, Aktienkurs-Beispiele)
- S. 14–22: Autokovarianz und Autokorrelation, ACF-Interpretation
- S. 23–27: Moving-Average-Prozesse
- S. 28–36: **AR-Prozesse** (Kern für Kap. 2.3.1)
- S. 37–44: ARMA/ARIMA, Box-Jenkins-Heuristik, ML-Schätzung

**Notation des Profs** (relevant für Konsistenz-Check im Theoriekapitel):
- AR(1): `X_t = φ · X_{t−1} + W_t` mit `|φ| < 1`
- AR(p): `X_t = Σ_{k=1..p} φ_k · X_{t−k} + W_t`
- White Noise: `W_t ~ N(0, σ²)` (nicht `ε_t`, nicht `a_t`)
- Analytische ACF eines AR(1): `ρ(h) = φ^h` (exponentieller Abfall)
- Analytische Autokovarianz AR(1): `γ(h) = φ^h · σ² / (1 − φ²)`
- ARMA(p,q): `X_t = Σ φ_k · X_{t−k} + W_t + Σ θ_k · W_{t−k}`
- ARIMA(p,d,q): d-fache Differenzbildung vor ARMA-Modellierung

**Box-Jenkins-Heuristik** (S. 43), die der Prof explizit lehrt:
- `d`: bilde Differenzen, solange Trend vorhanden
- `p`: größte Verzögerung mit empirischer PACF ≠ 0
- `q`: größte Verzögerung mit empirischer ACF ≠ 0
- Funktioniert gut für kleine p, q (`p + q ≤ 2`)

**Schätzverfahren** (S. 44): Maximum-Likelihood-Estimation als Standardansatz.

**Direkte Konsequenz für die Arbeit**:
1. **Zitierfähige Hauptquelle für Kap. 2.3.1**: Stollhoff, R. (2023): Theorie der ARIMA Prozesse. Vorlesungsunterlagen "BM-Fin Quantitative Methoden", TH Wildau, WS 2023/24.
2. **Notation überprüfen**: Wenn in Kap. 2.3.1 der Störterm `ε_t` heißt (statt `W_t`), genügt eine Fußnote zur Notationskonvention. Wichtiger ist Konsistenz innerhalb der Arbeit.
3. **PACF und Box-Jenkins**: Falls in Kap. 3 die AR-Ordnungswahl nicht erklärt ist (manuell via PACF/ACF vs. automatisch via `auto.arima` o. ä.), kurze Stelle ergänzen — der Prof prüft das explizit.
4. **Stationarität / Differenzbildung**: Der Prof betont die Differenzenstufe `d` als ersten Schritt. Falls die Kennzahlenanalyse auf Levels arbeitet (nicht auf ersten Differenzen), sollte Kap. 3 dies kurz begründen (z. B. mit Verweis auf Bilanz-/GuV-Kennzahlen, die als jahresfrequente Niveau-Reihen modelliert werden).

---

## 2. 1301 Lineare Regression — kommentiert (15 Seiten)

Kurzer Foliensatz zur OLS. Begleitmaterial, das für **Kap. 6 FF3 (Strukturvariablen-Regressionen)** als Methodenreferenz dienen kann — eher leichtgewichtig als Theoriequelle.

**Inhaltliche Kerne**:
- OLS-Herleitung über Minimierung der Residuenquadratsumme
- Geschlossene Lösung: `a = Cov(x,y) / Var(x)`, `b = ȳ − a · x̄`
- Bestimmtheitsmaß R² (S. 9–10)
- Variablentransformation und Standardisierung (S. 13): Abziehen des Mittelwerts, Teilen durch die Standardabweichung — als Hilfsmittel zur besseren Vergleichbarkeit von Koeffizienten

**Relevanz für die Arbeit**:
- Nicht stark genug als alleinige Methodenquelle für Kap. 6 — dort sind Fama/French-Logik und ggf. ein etablierter Ökonometrie-Text die bessere Referenz.
- Kann aber als sekundärer Verweis für Standardisierungslogik dienen, falls in Kap. 3.5/3.6 oder Kap. 6 die Strukturvariablen standardisiert werden.

---

## 3. Grundlagenkenntnisse Wahrscheinlichkeitsrechnung und Statistik (28 Seiten)

Schul-/Bachelor-Niveau-Repetitorium des Profs. Behandelt Wahrscheinlichkeitsrechnung, Zufallsvariablen, Binomial- und Normalverteilung, Lage- und Streuungsparameter, Kovarianz/Korrelation, kausale vs. statistische Zusammenhänge.

**Inhaltliche Kerne**:
- Dichtefunktion der Normalverteilung (S. 13): `f(x) = 1/(σ·√(2π)) · exp(−(x−μ)²/(2σ²))`
- 68-/95-/99-Heuristik (S. 14)
- Diskussion statistischer vs. kausaler Zusammenhänge (S. 27): "Ein statistischer Zusammenhang hat eine kausale Ursache" — interessant für die Vorsicht in FF2 (Lead-Lag) und FF3, dass aus Korrelation keine Kausalität folgt

**Relevanz für die Arbeit**:
- Nicht zitierfähig im Theoriekapitel (Schulwissen). Aber: die explizite Trennung statistisch ↔ kausal kann als kurzer Verweis in einer Limitierungs-Passage in FF2 oder FF3 dienen, wenn dort vor Kausal-Schlüssen aus Lead-Lag-Mustern gewarnt wird.

---

## 4. Theoretische Grundlagen Klassische Komponentenzerlegung (28 Seiten)

Foliensatz zum klassischen Zeitreihenansatz: Trend (gleitender Durchschnitt, exponentielle Glättung, lineare Regression), Saisonalität, Komponentenzerlegung. Methodisch Gegenpol zum AR-Ansatz.

**Inhaltliche Kerne**:
- Trendverfahren: gleitender Durchschnitt, exponentielle Glättung, lineare Trendregression
- Saisonale Komponentenzerlegung (additiv/multiplikativ) — eher für höherfrequente Daten relevant
- Holt-Winters

**Relevanz für die Arbeit**:
- Nicht direkt verwendet, aber wertvoll als **Abgrenzung in Kap. 3 (Methodenwahl)**: Der Prof unterrichtet beide Familien (klassische Zerlegung vs. stochastische ARIMA-Modelle). Eine Begründung, warum für jahresfrequente Finanzkennzahlen mit potenziell autoregressiver Persistenz das AR-Modell und nicht die klassische Komponentenzerlegung gewählt wurde, deckt eine erwartbare Prüferfrage ab.
- Insbesondere: Klassische Zerlegung setzt deterministische Trends voraus; Finanzkennzahlen sind eher als stochastische Prozesse mit Mean-Reversion (AR) plausibel.

---

## 5. Ergänzende Literatur (vom Prof empfohlen)

**Perlin, M. S. (2020): Analyzing Financial and Economic data with R**, 2. Aufl., vom Autor für den Kurs zur Verfügung gestellt (PDF-Wasserzeichen-Version, nicht weitergebbar).
- URL im Kurs: `pluginfile.php/529575/.../2020-AnaFinEcoDataR_ed_02_watermark.pdf`
- Englischsprachiger Standardtext für Finanzdaten-Analyse mit R; deckt ARIMA, GARCH, Portfolio
- Als Sekundärquelle in Kap. 3 oder Kap. 5.1 (Methodik der Drift-Analyse) zitierfähig

**Hyndman, R. J. & Athanasopoulos, G.: Forecasting: Principles and Practice** (3. Aufl., otexts.com/fpp3/)
- Frei online, Standardwerk für Zeitreihen-Vorhersage
- Vom Prof explizit empfohlen ("klare Empfehlung meinerseits")
- Behandelt ARIMA, ETS, Saisonalität, Hierarchical Forecasting; auf English
- Sehr starke Zweitquelle für Kap. 2.3.1 (AR-Modell) — international etabliert

---

## 6. Zusammenfassung — Was konkret in die Arbeit aufnehmen

**Kap. 2.3.1 (AR-Modell)**
- Stollhoff (2023) als deutsche Vorlesungs-Hauptquelle ergänzen
- Optional Hyndman/Athanasopoulos (fpp3) als internationale Zweitquelle
- Notation überprüfen: AR(p)-Schreibweise mit `φ_k` und `W_t` als White Noise ist die Prof-Notation
- Klärt sicher: explizite Erwähnung von ACF und PACF als analytische Werkzeuge

**Kap. 3 (Methodik)**
- Box-Jenkins-Heuristik vs. automatische Ordnungswahl kurz adressieren — welcher Pfad wurde gewählt und warum?
- Differenzenstufe `d` thematisieren (auch wenn `d=0` für Jahresfrequenz und Niveau-Daten plausibel ist, sollte das begründet werden)
- Kurze Abgrenzung zur klassischen Komponentenzerlegung als nicht gewählter Alternative (1–2 Sätze)
- ML-Schätzung als Standardverfahren benennen

**Kap. 5 (FF2) / Kap. 6 (FF3)**
- Trennung statistisch ↔ kausal: ggf. in Limitierungs-Passage einen Satz dazu, dass Lead-Lag-Korrelation (FF2) bzw. Strukturvariablen-Zusammenhänge (FF3) keine Kausalstruktur belegen

**Quellenkartei**
- Stollhoff, R. (2023): Theorie der ARIMA Prozesse. Vorlesungsunterlagen "BM-Fin Quantitative Methoden", TH Wildau, WS 2023/24
- Stollhoff, R. (2023): Theoretische Grundlagen Klassische Komponentenzerlegung. Vorlesungsunterlagen "BM-Fin Quantitative Methoden", TH Wildau, WS 2023/24
- Stollhoff, R. (2023): Lineare Regression. Vorlesungsunterlagen "BM-Fin Quantitative Methoden", TH Wildau, WS 2023/24
- Perlin, M. S. (2020): Analyzing Financial and Economic Data with R. 2. Aufl.
- Hyndman, R. J. & Athanasopoulos, G. (3. Aufl.): Forecasting: Principles and Practice. https://otexts.com/fpp3/

---

## 7. Nicht relevant für die Arbeit

- Portfolioanalyse / -optimierung (Sharpe, Tangentenportfolio, fPortfolio, Markowitz) — komplett anderes Themenfeld
- R-Tutorials, ggplot2, R Markdown, RStudio-Bedienung, Cheatsheets — Werkzeug
- Quantmod / Yahoo-Datenabruf
- GARCH (nur relevant falls σ-Dimension in Kap. 4.3 als bedingte Varianz formal modelliert wird; aktuell deskriptiv via Stichproben-Standardabweichung — also nicht nötig)
- Hausarbeiten / Übungsaufgaben des Kurses — eigene Übungsleistung, keine Methodenreferenz
- Wang & Strong (1996) zu Datenqualität — eher tangential

---

## Anmerkungen

- Inhalte basieren ausschließlich auf den vier extrahierten PDFs (ARIMA-kommentiert 44 S., 1301 LinReg-kommentiert 15 S., Statistik-Grundlagen 28 S., Komponentenzerlegung 28 S.) sowie der Kursübersicht.
- Die einzelnen ARIMA-Teile (Teil 1, 2, 4) sind im Kurs als Vorlesungs-**Videos** (mp4) hinterlegt — nicht als separate PDFs. Die kommentierte Gesamtversion enthält jedoch alle Inhalte als Folien.
- Perlin-PDF wurde nicht extrahiert (Buchformat, ca. 500+ Seiten); URL gesichert.
- Hyndman: Standardlink ist https://otexts.com/fpp3/ (3. Auflage, frei).
