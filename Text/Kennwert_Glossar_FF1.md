# Kennwert-Glossar — Statistische Größen in FF1

**Stand:** 26.04.2026
**Zweck:** Für jeden Wert, den Du in Kapitel 4 verwendest, eine knappe Referenz: wie er berechnet wird, wo er in Deiner Arbeit auftaucht, was er aussagt, und welche Faustregeln gelten. Mit Beispielzahlen aus Deinem eigenen Datensatz.

---

## Inhalt

**A. AR-Modellparameter** — φ₁, φ₂, c, ε, σ(ΔY)
**B. Modellgüte** — R², p-Wert, Signifikanzrate, AIC/BIC, Log-Likelihood
**C. Abgeleitete Größen** — Halblebensdauer t½, erste Differenzen ΔY, saisonale Differenzen Δ₄Y, Log-Returns
**D. Verteilungs-Statistiken** — Mittelwert, Median, Standardabweichung, IQR, Perzentile
**E. Korrelations- und Test-Statistiken** — Spearman ρ, χ²-Test, Wilcoxon, Bonferroni
**F. Konzepte** — Lag-Operator, ACF, Stationarität, Mean-Reversion vs. Persistenz vs. Momentum

---

## A. AR-Modellparameter

### A.1 φ₁ — der AR(1)-Koeffizient

**Formel.** Das AR(1)-Modell lautet in Deiner Spezifikation:

> ΔY(t) = c + φ₁ · ΔY(t−1) + ε(t)

φ₁ ist der Steigungs-Koeffizient einer einfachen OLS-Regression der Variable auf ihren eigenen Vorquartalswert (1 Lag). Wird je Unternehmen × Kennzahl-Paar individuell geschätzt.

**Wo in Deiner Arbeit.** Hauptkennzahl überall — Tab. 4.1 (Querschnittsmediane), 4.2a–g (pro Kennzahl), 4.3, 4.4 (Sektor × Kennzahl), 4.5 (Modellvergleich), 4.6 (Stichprobenrobustheit), 4.7 (Trennbarkeitsprüfung).

**Was er aussagt.** Wie stark eine quartalsweise Veränderung im Folgequartal zurückgenommen oder verstärkt wird.

| φ₁-Bereich | Interpretation | Beispiel aus Deiner Arbeit |
|---|---|---|
| φ₁ ≈ 0 | Kein systematisches Muster — Veränderungen sind quasi-zufällig | EK-Quote: φ₁ = −0,04 |
| 0 < φ₁ < +1 | **Persistenz / Momentum** — eine Veränderung wird im Folgequartal anteilig fortgesetzt | EK-Quote auf Levels: φ₁ = +0,93 |
| −1 < φ₁ < 0 | **Mean-Reversion** — eine Veränderung wird im Folgequartal anteilig korrigiert | ROA: φ₁ = −0,43 |
| φ₁ → −1 oder +1 | Sehr starke Korrektur bzw. Persistenz; nahe ±1 ist die Reihe instationär | (in Deinen Daten nicht erreicht) |

**Faustregel.** Stationarität verlangt |φ₁| < 1. Werte um −0,5 sind starke Korrektur, Werte um −0,1 sind schwache Korrektur, Werte um 0 bedeuten White-Noise-artige Veränderungen.

**Im Video.** Der Prof spricht von "den Koeffizienten, die hier berechnet werden" und meint genau φ₁ (und ggf. φ₂, ...). Sein Modell läuft auf einer Zeitreihe — er bekommt einen φ₁-Wert. Du bekommst 932 davon pro Kennzahl.

---

### A.2 φ₂ — der AR(2)-Koeffizient (zweiter Lag)

**Formel.** Im AR(2)-Modell auf Differenzen:

> ΔY(t) = c + φ₁ · ΔY(t−1) + φ₂ · ΔY(t−2) + ε(t)

**Wo in Deiner Arbeit.** Nur in 4.5.1 als Robustheits-Spezifikation (Spalte „AR(2) auf diff1" in Tab. 4.5).

**Was er aussagt.** Ob es eine zusätzliche Korrekturdynamik im *zweiten* zurückliegenden Quartal gibt, die das AR(1)-Modell unterschätzt.

**Befund Deiner Arbeit.** Bei Profitabilität wird die Mean-Reversion unter AR(2) deutlich stärker (Median φ₁ wandert von −0,43 auf −0,55, R² steigt von 0,18 auf 0,29). Daraus folgt: AR(1) ist eine konservative Schätzung — Du unterzeichnest die Mean-Reversion eher, als sie zu übertreiben.

---

### A.3 c — die Konstante (Drift-Term)

**Formel.** Der Achsenabschnitt der OLS-Regression.

**Was er aussagt.** Bei Differenzen-Modellen interpretierbar als durchschnittliche Quartalsveränderung, die nicht durch das Lag erklärt wird — eine Art "Drift".

**Wo in Deiner Arbeit.** Im Modell vorhanden, in den Tabellen aber nicht explizit ausgewiesen, weil bei Differenzen ökonomisch wenig informativ und meist nahe null.

**Faustregel.** Bei stationären Differenzen sollte c klein sein. Wenn nicht, hat die Originalreihe einen systematischen Trend, der durch die Differenzbildung nicht restlos entfernt wurde.

---

### A.4 ε(t) — das Residuum (Schock)

**Formel.** ε(t) = ΔY(t) − c − φ₁ · ΔY(t−1)

Das, was vom AR(1)-Modell **nicht** erklärt wird. Bei einem gut spezifizierten Modell sind die Residuen weißes Rauschen (kein Muster mehr).

**Wo in Deiner Arbeit.** Direkt nicht ausgewiesen, aber σ(ΔY) misst seine Streuung; in 4.5.5 (Asymmetrie der Mean-Reversion) wäre ε(t) das Objekt der Untersuchung — Aufteilung nach Vorzeichen des vorigen Schocks.

**Was es aussagt.** Die "Innovation" im Quartal — der Anteil der Veränderung, der nicht aus dem Vorquartal vorhergesagt werden konnte.

---

### A.5 σ(ΔY) — Standardabweichung der Veränderungen

**Formel.** Die Standardabweichung der ersten Differenzen ΔY(t) über die Zeit, je Unternehmen × Kennzahl.

> σ(ΔY) = √( (1/(T−1)) · Σ (ΔY(t) − ΔȲ)² )

**Wo in Deiner Arbeit.** Zweite Quadrantendimension. Tab. 4.1 (Median σ pro Kennzahl), 4.2a–g (pro Kennzahl), Tab. 4.3b (sektoral), Tab. 4.7 (Spearman vs. φ₁).

**Was er aussagt.** Wie stark die Quartalsveränderungen einer Kennzahl streuen — ein Maß für die "Schwankungsexposition" des Unternehmens auf dieser Kennzahl.

**Wichtige Eigenschaft.** σ(ΔY) ist konstruktionsbedingt ≥ 0 und meist rechtsschief verteilt — es gibt einzelne Firmen mit sehr hohen σ-Werten, die den Mittelwert nach oben ziehen. Daher in Deinen Tabellen sinnvollerweise *Median* + *Mittelwert* + *p5/p95* nebeneinander.

**Beispiel.** ROA: σ-Median 0,017 → typische Quartalsschwankungen liegen bei ±1,7 Prozentpunkten. Real Estate FCF-Marge: σ = 0,601 → Faktor 6 über dem Gesamtmedian.

**Im Video.** Der Prof berechnet "die Volatilität der Returns" — das ist exakt dasselbe: Standardabweichung der ersten Differenzen (Log-Returns sind im Wesentlichen Differenzen).

---

## B. Modellgüte

### B.1 R² — Bestimmtheitsmaß

**Formel.** R² = 1 − SS_res / SS_tot, wobei SS_res die Quadratsumme der Residuen, SS_tot die Quadratsumme der Abweichungen vom Mittelwert ist.

**Wertebereich.** 0 ≤ R² ≤ 1.

**Wo in Deiner Arbeit.** Tab. 4.1 (R²-Verteilung pro Kennzahl), 4.2a–g (R²-IQR), Abb. 4.2 (R²-Verteilung als Boxplot/KDE), Tab. 4.5 (Modellvergleich).

**Was es aussagt.** Welcher Anteil der Quartalsvarianz durch das AR(1)-Modell erklärt wird.

**Interpretation Deiner Werte.**
- ROA-R²-Median ≈ 0,19 → das AR(1)-Modell erklärt rund 19 % der Quartalsvarianz. Solider Wert für ein univariates Zeitreihenmodell auf Quartalsdaten (Hamilton 1994).
- EK-Quote-R²-Median ≈ 0,008 → das AR(1)-Modell erklärt praktisch nichts. Bestätigt den Nullbefund der Bilanzstruktur-Mean-Reversion.

**Faustregel.** Bei univariaten AR(1)-Modellen auf Quartalsdaten sind R²-Werte über 0,15 bereits gut. Niedrige R² sind kein Modellversagen, sondern selbst ein Befund (sagt: "Es gibt keine systematische Lag-1-Struktur in dieser Reihe").

**Im Video.** Der Prof zeigt R² nicht explizit, aber wenn er sagt "das haut nicht so wirklich hin" beim Forecast, ist das implizit ein R²-Argument — das Modell erklärt zu wenig der Variation.

---

### B.2 p-Wert (für φ₁)

**Berechnung.** Der p-Wert testet H₀: φ₁ = 0 gegen H₁: φ₁ ≠ 0. Unter H₀ folgt der t-Wert (φ₁/SE(φ₁)) annähernd einer t-Verteilung mit T−2 Freiheitsgraden. Der p-Wert ist die Wahrscheinlichkeit, einen mindestens so extremen t-Wert zu beobachten, wenn H₀ wahr ist.

**Wo in Deiner Arbeit.** Implizit in Sig.-Rate; explizit für die Beispielfirmen in Tab. 4.10 ("p < 0,001" für Walmart/Boeing/MSFT, "0,010" für Amazon).

**Was er aussagt.** Wie sicher Du sein kannst, dass φ₁ wirklich von null verschieden ist (also es eine echte Mean-Reversion oder Momentum gibt) und nicht nur ein Zufallsbefund ist.

**Faustregel.**
- p < 0,001 → sehr stark signifikant
- p < 0,05 → signifikant (Standardgrenze)
- p ≥ 0,05 → nicht signifikant; φ₁ ist statistisch nicht von null unterscheidbar

---

### B.3 Signifikanzrate

**Berechnung.** Anteil der Unternehmen, deren individueller AR(1)-Koeffizient bei p < 0,05 signifikant ist.

> Sig.% = (Anzahl Firmen mit p < 0,05) / (Gesamtzahl Firmen) · 100

**Wo in Deiner Arbeit.** Tab. 4.1 ("Sig."-Spalte), Tab. 4.3c (sektoral), Abb. 4.2 (links).

**Was sie aussagt.** Wie verbreitet ein Befund über das Panel ist. Eine Sig.-Rate von 92 % bei ROA bedeutet: Der Mean-Reversion-Befund ist nicht nur ein Mittelwert-Effekt, sondern eine fast universelle Eigenschaft der Kennzahl — er gilt für 9 von 10 Firmen einzeln signifikant.

**Faustregel.**
- Sig.% > 80 % → sehr robuste Eigenschaft
- Sig.% 40–60 % → uneinheitlich, sektoral verteilt
- Sig.% < 30 % → das Modell greift kennzahlenweit kaum (Bilanzstruktur)

**Beispiel Hierarchie aus Deinen Daten.** FCF-Marge 96,6 % → ROA 92,2 % → Current Ratio 45,6 % → EK-Quote 18,6 %. Reproduziert die Drei-Dynamiktypen-Hierarchie unabhängig vom φ₁-Median.

---

### B.4 AIC / BIC — Informationskriterien (im Video angedeutet)

**Formeln.**
- AIC (Akaike) = 2k − 2·ln(L), wobei k die Parameteranzahl ist und L die Likelihood
- BIC (Bayes/Schwarz) = k·ln(T) − 2·ln(L), wobei T die Anzahl Beobachtungen ist

**Was sie aussagen.** Modellgüte bei gleichzeitiger Bestrafung von Komplexität. Bei Vergleich mehrerer Modelle: kleineres AIC/BIC ist besser. BIC bestraft zusätzliche Parameter stärker als AIC.

**Wo in Deiner Arbeit.** Aktuell nicht explizit verwendet — Du vergleichst Modelle in 4.5.1 über Median-φ₁ und Sig.%. Wenn Dich der Prof fragt, "Warum nicht AIC?", lautet die saubere Antwort: AIC/BIC vergleichen Modelle *für eine Zeitreihe*. Du vergleichst Modelle *im Querschnitt über 932 Reihen*. Aggregierte Mediane von R² und Sig.-Rate sind hier informativer als ein aggregiertes AIC.

**Im Video.** Wenn der Prof von "deskriptiven Maßen" und einem "leck value von 26" spricht, meint er wahrscheinlich Log-Likelihood oder AIC/BIC, die `statsmodels` standardmäßig mit ausgibt.

---

### B.5 Log-Likelihood (ln L)

**Was es ist.** Der Logarithmus der Likelihood-Funktion am Maximum. Misst, wie wahrscheinlich die beobachteten Daten unter dem geschätzten Modell sind.

**Wo in Deiner Arbeit.** Implizit Bestandteil der OLS-Schätzung, aber nicht explizit ausgewiesen.

**Was es aussagt.** Höhere Log-Likelihood = besseres Modell. Allein nicht aussagekräftig — nur im Vergleich (über AIC/BIC oder Likelihood-Ratio-Tests).

---

## C. Abgeleitete Größen

### C.1 t½ — Halblebensdauer (Half-Life)

**Formel.**

> t½ = ln(0,5) / ln(1 + φ₁)

Gilt nur für negative φ₁ (Mean-Reversion). Für φ₁ ≥ 0 wäre t½ undefiniert oder negativ.

**Wo in Deiner Arbeit.** Tab. 4.1 (zwei Spalten: t½ Q und t½ J), als Verstärker-Argument 1 in 4.3.1.

**Was sie aussagt.** Nach wie vielen Quartalen ein Schock im Median zur Hälfte abgebaut ist. Übersetzt den abstrakten φ₁-Wert in eine ökonomisch greifbare Zeitdimension.

**Beispielrechnung.**
- ROA: φ₁ = −0,43 → t½ = ln(0,5)/ln(0,57) = −0,693 / −0,562 ≈ **1,23 Quartale ≈ 0,31 Jahre**
- D/E: φ₁ = −0,089 → t½ = ln(0,5)/ln(0,911) ≈ **7,4 Quartale ≈ 1,85 Jahre**
- EK-Quote: φ₁ = −0,040 → t½ ≈ **17 Quartale ≈ 4,3 Jahre**

**Argumentationswert.** Die Spreizung um Faktor 15 zwischen oberster (1,2 Q) und unterster Schicht (17 Q) ist Dein quantitatives Argument für die Drei-Dynamiktypen-Hierarchie als ökonomisch tragfähig.

**Im Video.** Wird nicht behandelt — der Prof bleibt auf Modellebene.

---

### C.2 ΔY(t) — Erste Differenzen

**Formel.** ΔY(t) = Y(t) − Y(t−1)

**Wo in Deiner Arbeit.** Die zentrale Transformation Deines Hauptmodells. Sämtliche Schätzungen laufen auf ΔY, nicht auf Y.

**Warum.** Levels-Reihen von Finanzkennzahlen sind in der Regel **instationär** (haben Trends, Strukturbrüche, sich verschiebende Mittelwerte). Differenzen entfernen diese Niveaupersistenz und machen die Reihe stationär — Voraussetzung für korrekte AR-Inferenz.

**Was sie aussagt.** Die Quartal-zu-Quartal-Veränderung. Statt zu fragen "Wie hoch ist die Marge?" fragst Du "Wie hat sich die Marge verändert?".

**Im Video.** Der Prof macht dasselbe mit Log-Returns: log(P_t) − log(P_{t−1}) ist die erste Differenz der logarithmierten Preisreihe. Er sagt selbst: "wenn wir die Returns berechnen, können wir die Autokorrelation deutlich reduzieren" — exakt das Argument für Differenzbildung.

---

### C.3 Δ₄Y(t) — Saisonale Differenzen (4-Quartals-Differenz)

**Formel.** Δ₄Y(t) = Y(t) − Y(t−4)

**Wo in Deiner Arbeit.** Nur in 4.5.1 als Robustheits-Spezifikation („Δ₄Y" / „diff4" in Tab. 4.5).

**Was sie aussagt.** Die Veränderung gegenüber dem **gleichen Quartal des Vorjahres** — entfernt saisonale Effekte (Q4-Jahresend-Effekte, Q1-Saisonschwächen, etc.).

**Befund Deiner Arbeit.** Unter Δ₄Y werden die φ₁-Werte positiv (z.B. ROA: +0,21 statt −0,43). Das ist plausibel: Auf Jahresbasis dominieren persistente Niveauveränderungen, weil saisonale Kurzfrist-Korrekturen herausgenommen sind.

---

### C.4 Log-Returns (im Video, in Deiner Arbeit nicht zentral)

**Formel.** r(t) = ln(P(t)) − ln(P(t−1)) = ln(P(t)/P(t−1))

**Was sie aussagen.** Die kontinuierlich verzinste Rendite. Vorteil gegenüber einfachen Renditen: addieren sich linear über die Zeit, sind annähernd normalverteilt für kleine Werte.

**Bezug zu Deiner Arbeit.** Du verwendest **keine** Log-Returns, weil Deine Kennzahlen (ROA, EK-Quote etc.) **Quoten** sind, keine Preise. Bei Quoten würden Log-Differenzen die Interpretation verzerren — Du nimmst stattdessen einfache Differenzen.

**Wenn Du gefragt wirst.** "Warum keine Log-Differenzen?" → "Weil meine Variablen bereits Quoten sind. Eine Log-Differenz wäre ökonomisch schwer zu interpretieren (Veränderung eines Quotienten in Prozentpunkten ist intuitiver als ihre Log-Differenz)."

---

## D. Verteilungs-Statistiken (Querschnitts-Aggregation)

Diese Statistiken aggregieren die individuellen φ₁- (oder σ-) Schätzungen über alle 932 Unternehmen.

### D.1 Mittelwert (arithmetisch)

**Formel.** x̄ = (1/n) · Σ xᵢ

**Wo.** Tab. 4.1 ("φ₁ Ø", "σ(ΔY) Ø"), Tab. 4.2a–g.

**Was er aussagt.** Der Schwerpunkt der Verteilung. Empfindlich gegen Ausreißer.

**Wann verwenden.** Wenn Du eine "Gesamtsumme dividiert durch n"-Aussage brauchst (z.B. "Das durchschnittliche Unternehmen hat φ₁ = ..."). Bei rechtsschiefen Verteilungen (σ-Werte!) liegt der Mittelwert deutlich über dem Median — daher Median + Mittelwert nebeneinander berichten.

---

### D.2 Median

**Berechnung.** Der Wert, der die geordnete Stichprobe in zwei gleich große Hälften teilt (50.-Perzentil).

**Wo.** Tab. 4.1 ("φ₁ Md"), Tab. 4.3 (Sektor-Mediane), überall als Hauptkennzahl.

**Was er aussagt.** Das "typische" Unternehmen. Robust gegen Ausreißer.

**Warum Du ihn als Hauptkennzahl nimmst.** Bei 932 Firmen und σ-Verteilungen mit Faktor 28 zwischen p5 und p95 würde der Mittelwert von einzelnen Extremfirmen verzerrt. Der Median ist die ehrlichere Hierarchie-Aussage.

---

### D.3 Standardabweichung (Querschnitt)

**Formel.** σ_x = √( (1/(n−1)) · Σ (xᵢ − x̄)² )

**Wo.** Tab. 4.1 ("φ₁ σ", "σ(ΔY) σ"), Tab. 4.2a–g ("Std. Abweichung").

**Was sie aussagt.** Wie weit die individuellen Schätzungen um den Mittelwert streuen. Hilfreich, um zu sagen "ROA hat φ₁ = −0,43 bei Streuung 0,14 — also liegen rund 68 % der Firmen im Bereich [−0,57; −0,29]".

**Vorsicht.** Die "68 %"-Regel gilt nur, wenn die Verteilung näherungsweise normal ist. Bei rechtsschiefen σ-Verteilungen besser p5/p95 statt ±1·SD nutzen.

---

### D.4 IQR — Interquartilsabstand

**Berechnung.** IQR = Q3 − Q1 = 75.-Perzentil − 25.-Perzentil. Enthält die mittleren 50 % der Daten.

**Wo.** Tab. 4.2a–g ("IQR" mit eckigen Klammern, z.B. ROA-φ₁-IQR = [−0,503; −0,333]).

**Was er aussagt.** Wie eng die "Mitte" der Verteilung liegt. Robust gegen Ausreißer (im Gegensatz zur Standardabweichung).

**Verwendungstipp.** Wenn Du sagen willst "drei Viertel der Firmen liegen zwischen −0,50 und −0,33" — das macht die Konsistenz Deiner Hauptbefunde anschaulich. Du tust das in 4.1.2 für ROA bereits sehr gut.

---

### D.5 5./95. Perzentil

**Berechnung.** Die Werte, unter denen 5 % bzw. 95 % der Stichprobe liegen.

**Wo.** Tab. 4.2a–g ("5./95. Perzentil").

**Was sie aussagen.** Die "Ränder" der Verteilung — das obere und untere 5 %. Hilfreich, um zu zeigen, dass selbst die extremsten Firmen noch im erwarteten Bereich liegen.

**Beispiel aus Deiner Arbeit.** ROA-φ₁: [−0,610; −0,163] → selbst am 95. Perzentil bleibt φ₁ deutlich negativ. Das ist ein starkes Argument: "Es ist nicht so, dass nur ein paar Firmen Mean-Reversion zeigen — fast alle tun es."

---

## E. Korrelations- und Test-Statistiken

### E.1 Spearman-Rangkorrelation ρ

**Formel.** Korrelation der **Ränge** zweier Variablen statt ihrer Werte. Wenn x_i und y_i die Ränge sind:

> ρ = 1 − (6 · Σ d_i²) / (n · (n² − 1)),  mit d_i = Rang(x_i) − Rang(y_i)

**Wertebereich.** −1 ≤ ρ ≤ +1.

**Wo in Deiner Arbeit.** Tab. 4.7 (φ₁ × σ(ΔY) pro Kennzahl).

**Was er aussagt.** Wie stark zwei Variablen monoton zusammenhängen — ohne Annahme einer linearen Beziehung. Robuster als Pearson, weil ausreißerresistent.

**Warum Spearman statt Pearson?** Deine φ₁- und σ-Verteilungen sind nicht streng normalverteilt; σ ist deutlich rechtsschief. Pearson wäre verzerrt.

**Faustregel (Rucker et al. 2015 — Deine Quelle).**
- |ρ| < 0,3 → schwache Kopplung; Median-Split über zwei Dimensionen vertretbar
- 0,3 ≤ |ρ| < 0,5 → moderate Kopplung; Vorsicht
- |ρ| ≥ 0,5 → starke Kopplung; eindimensionale Analyse vorzuziehen

**Befund Deiner Arbeit.** Profitabilität: |ρ| < 0,19 (sehr schwach), Bilanzstruktur: 0,19 ≤ |ρ| ≤ 0,24 (schwach). Quadrantenklassifikation methodisch verteidigbar.

---

### E.2 χ²-Test (Chi-Quadrat-Test auf Gleichverteilung)

**Formel.** Unter H₀: gleichmäßige Verteilung über k Kategorien:

> χ² = Σ (Beobachtet − Erwartet)² / Erwartet

mit (k−1) Freiheitsgraden.

**Wo in Deiner Arbeit.** Tab. 4.8 — Test, ob die vier Quadranten gleich besetzt sind (Erwartungswert = n/4 pro Zelle).

**Was er aussagt.** Wenn der Test signifikant ist (p < 0,05), unterscheidet sich die beobachtete Verteilung von der erwarteten Gleichverteilung — die Quadranten sind also gekoppelt (eine zweite Bestätigung der Spearman-Korrelation).

**Befund Deiner Arbeit.** 4 von 7 Kennzahlen unauffällig (Quadranten gleich besetzt), 3 (EBIT-Marge, Current Ratio, D/E) signifikant abweichend (Korrektiv-Volatil und Persistent-Stabil überrepräsentiert). Das ist die ehrliche Einschränkung der Trennbarkeit, die Du in 4.4 als "Beitragsdimension 3 — bestätigt mit Einschränkung" aufnimmst.

---

### E.3 Wilcoxon-Vorzeichen-Rang-Test (für 4.5.4 geplant)

**Formel.** Test, ob zwei abhängige Stichproben (z.B. φ₁-Werte derselben Firma in zwei Halbperioden) systematisch verschieden sind. Robust, da nicht-parametrisch.

**Wo in Deiner Arbeit.** In 4.5.4 vorgesehen für den Halbperioden-Vergleich (Pre/Post-Finanzkrise) — aktuell als Platzhalter.

**Was er aussagen wird.** Ob sich die Mean-Reversion-Stärke einer Kennzahl zwischen 2000–2012 und 2013–2024 statistisch signifikant verschoben hat.

---

### E.4 Bonferroni-Korrektur

**Formel.** Wenn Du m Tests gleichzeitig durchführst, korrigiere die Signifikanzschwelle:

> α_korrigiert = α / m

**Wo in Deiner Arbeit.** Übergang zu Kap. 5 angekündigt: für die 42 Paartests in der φ₁- und σ-Korrelationsmatrix wird α = 0,05 / 42.

**Warum.** Bei vielen parallelen Tests steigt die Wahrscheinlichkeit eines falsch-positiven Befunds (Familienfehler-Rate). Bonferroni ist konservativ und verteidigbar.

---

## F. Konzepte (kein Wert, aber wichtig zu verstehen)

### F.1 Lag-Operator L

**Definition.** L · Y(t) = Y(t−1). Lⁿ · Y(t) = Y(t−n).

**Wo.** Wird in Lehrbüchern für die kompakte Schreibweise von ARMA-Modellen genutzt:

> AR(1): (1 − φ₁L) · Y(t) = c + ε(t)

**Im Video.** Der Prof spricht von "den falschen Lag-Operator" — meint, dass das Modell vielleicht mehr als nur den 1-Lag bräuchte.

**In Deiner Arbeit.** Nicht explizit verwendet, aber implizit: φ₁ ist der Koeffizient des Lag-1-Terms; in 4.5.1 unter AR(2) auch φ₂ am Lag-2.

---

### F.2 Autokorrelationsfunktion (ACF)

**Definition.** ACF(k) = Korrelation von Y(t) mit Y(t−k) für verschiedene Lag-Tiefen k.

**Wo im Video.** Der Prof plottet die ACF, um zu sehen "wie auto-korreliert" die Reihe ist — ein klassisches Diagnose-Werkzeug vor jeder Modellwahl.

**In Deiner Arbeit.** Du nutzt nicht die ACF-Plots im Kapitel selbst, weil bei 932 Firmen × 7 Kennzahlen jeweils ein eigenes ACF-Bild absurd wäre. Stattdessen nutzt Du **direkt** das Ergebnis: φ₁ aus dem AR(1)-Fit ist genau die Lag-1-Autokorrelation der differenzierten Reihe. Wenn Dich der Prof fragt "Hast Du die ACF angeschaut?" — die ehrliche Antwort: φ₁ **ist** die geschätzte Lag-1-Autokorrelation.

---

### F.3 Stationarität

**Definition.** Eine Zeitreihe ist (schwach) stationär, wenn:
- Mittelwert konstant über die Zeit
- Varianz konstant über die Zeit
- Kovarianz Cov(Y_t, Y_{t−k}) hängt nur von k ab, nicht von t

**Warum es wichtig ist.** AR-Modelle setzen Stationarität voraus. Auf instationären Reihen sind φ₁-Schätzer verzerrt, R²-Werte aufgeblasen, p-Werte unzuverlässig (sog. spurious regression).

**Deine Lösung.** Erste Differenzen erzwingen Stationarität — das ist der zentrale methodische Schritt in 3.2.1 / 4.5.1 (Levels-Vergleich zeigt, warum die Differenzen-Wahl richtig ist).

---

### F.4 Mean-Reversion vs. Persistenz vs. Momentum (Vokabel-Klärung)

**Mean-Reversion:** Eine Veränderung wird im Folgezeitraum **zurückgenommen**. φ₁ < 0 auf Differenzen, oder 0 < φ₁ < 1 auf Levels (Rückkehr zum Mittelwert).

**Persistenz:** Eine Veränderung **bleibt** weitgehend erhalten. φ₁ ≈ 0 auf Differenzen (kein Korrekturmuster), oder φ₁ → 1 auf Levels (Random Walk).

**Momentum:** Eine Veränderung wird im Folgezeitraum **fortgesetzt** / verstärkt. φ₁ > 0 auf Differenzen.

**Warum die Differenzen-Lesart wichtig ist.** Auf Levels haben Bilanzstrukturkennzahlen φ₁ ≈ 0,93 (sehr persistent — ein Niveau wird gehalten). Auf Differenzen haben sie φ₁ ≈ −0,04 (kein systematisches Korrekturmuster der Veränderungen). Beides ist konsistent: Bilanzen ändern sich selten, aber wenn sie es tun, ist die Änderung quasi-zufällig (kein Folge-Muster).

**In Deiner Arbeit.** Du operierst durchgehend in der Differenzen-Lesart und nutzt deshalb präzise:
- Profitabilität → Mean-Reversion (Veränderungen werden korrigiert)
- Liquidität → Übergangszone (teilweise Mean-Reversion)
- Kapitalstruktur → Persistenz (Veränderungen sind quasi-zufällig)

---

## Schnellreferenz für Verteidigung / Fragen

| Wenn der Prof fragt... | Antworte ungefähr... |
|---|---|
| Warum AR(1) und nicht AR(p)? | Parsimonie. AR(2)-Robustheit (4.5.1) zeigt, dass die Hierarchie qualitativ bestehen bleibt — AR(1) ist konservative Schätzung. |
| Warum Differenzen, nicht Levels? | Stationarität. 4.5.1 zeigt zudem die komplementäre Lesart auf Levels — kein Widerspruch, andere Frage. |
| Warum Median, nicht Mittelwert? | Robust gegen rechtsschiefe σ-Verteilungen. Mittelwert in Tab. 4.1 zusätzlich ausgewiesen. |
| Warum Spearman, nicht Pearson? | Nichtparametrisch, robust gegen Verteilungsform. |
| Warum kein AIC/BIC im Modellvergleich? | Aggregate Median-R² und Sig.-Rate über 932 Reihen sind im Querschnitt informativer als ein aggregiertes AIC. |
| Was sagt φ₁ = −0,43? | Eine Quartalsveränderung wird im Folgequartal im Mittel zu 43 % zurückgenommen. Halblebensdauer ≈ 1,2 Quartale. |
| Wie zuverlässig ist der Befund auf Einzelfirmenebene? | Sig.-Rate. Bei Profitabilität > 90 % der Firmen einzeln signifikant — Hierarchie ist nicht nur Mittelwert-Effekt. |
| Warum keine Log-Returns? | Variablen sind Quoten, keine Preise. Differenzen interpretieren sich in Prozentpunkten — direkt ökonomisch lesbar. |

---

**Praktischer Tipp.** Wenn Du diese Übersicht beim Schreiben am Bildschirm offen hast, kannst Du im Fließtext kurz die Bedeutung eines Wertes erklären und mit einem Verweis ("vgl. Kennwert-Glossar §A.1") auf die Tiefenerklärung verweisen — ohne den Lesefluss zu zerstören. Für die Verteidigung dient dieselbe Datei als Spickzettel.
