# Test-Glossar — Statistische Tests in FF1

**Stand:** 26.04.2026
**Zweck:** Für jeden Test, den Du in Kapitel 4 (und vorbereitend in Kap. 5/6) anwendest: Was er testet, wie er rechnet, welche Annahmen er stellt, welche Alternativen es gäbe und warum genau dieser Test bei Dir die beste Wahl ist. Mit konkretem Bezug zu Deinen Tabellen.

---

## Inhalt

1. **t-Test auf den AR(1)-Koeffizienten** (in jedem Modell-Fit, ergibt p-Wert je Firma)
2. **Spearman-Rangkorrelation** (Tab. 4.7 — Trennbarkeit φ₁ × σ)
3. **χ²-Test auf Gleichverteilung** (Tab. 4.8 — Quadrantenbesetzung)
4. **χ²-Test auf Unabhängigkeit** (Kap. 6 — Sektor × Quadrant)
5. **Cramér's V** (Effektstärke für χ²-Tests; Prof-Entscheidung 26.03.2026)
6. **Wilcoxon-Vorzeichen-Rang-Test** (geplant für 4.5.4 — Halbperioden-Vergleich)
7. **Threshold-AR(1)** / Vorzeichen-Split (geplant für 4.5.5 — Asymmetrie-Test)
8. **Bonferroni-Korrektur** (Multiple Testing, Übergang zu Kap. 5)
9. **Test-Auswahllogik** (Entscheidungsbaum)
10. **Was Du bewusst NICHT testest** (mit Begründung)

---

## Vorbemerkung — Die Test-Auswahllogik in einem Bild

Bevor Du in die Einzelheiten gehst, lohnt eine Orientierung. Statistische Tests gliedern sich nach drei Achsen:

| Achse | Optionen | Konsequenz |
|---|---|---|
| **Datentyp** | metrisch / ordinal / kategorial | bestimmt verwendbare Testklasse |
| **Verteilungsannahme** | parametrisch (z.B. Normalverteilung) / nicht-parametrisch | parametrisch ist mächtiger, aber bricht bei Verstößen |
| **Stichproben-Beziehung** | unabhängig / gepaart (verbunden) | gepaarte Tests sind bei Wiederholungsmessungen mächtiger |

In Deiner Arbeit dominieren **nicht-parametrische** Tests, weil:
- Deine Verteilungen (insbesondere σ-Werte) sind rechtsschief und nicht normal
- Du hast n = 932 Firmen, und kleine Verstöße werden bei großem n statistisch sichtbar — nicht-parametrische Tests sind robuster
- Deine Variablen sind ordinal interpretierbar (Ränge sind ökonomisch sinnvoll: "Firma X hat stärkere Mean-Reversion als Firma Y")

Daher: **Spearman statt Pearson, Wilcoxon statt t-Test, χ² für Kategorien.**

---

## 1. t-Test auf den AR(1)-Koeffizienten

### Was er testet

H₀: φ₁ = 0 (kein systematischer AR-Effekt — die Veränderung ist White Noise)
H₁: φ₁ ≠ 0 (es gibt einen systematischen Lag-1-Zusammenhang)

### Wie er rechnet

Für jede einzelne Schätzung:

> t = φ̂₁ / SE(φ̂₁)

mit SE(φ̂₁) = Standardfehler aus der OLS-Kovarianzmatrix. Unter H₀ folgt t einer t-Verteilung mit (T − 2) Freiheitsgraden, in Deinem Fall T = 100 Quartale.

Der p-Wert ist die zweiseitige Wahrscheinlichkeit, einen mindestens so extremen t-Wert zu beobachten, wenn H₀ wahr wäre.

### Annahmen

1. Residuen ε(t) sind unabhängig und normalverteilt
2. Homoskedastizität (konstante Varianz)
3. Keine seriellen Autokorrelationen höherer Ordnung in den Residuen

### Warum er bei Dir gut passt

- Bei T = 100 ist die t-Verteilung nahezu normal — Annahme 1 ist robust
- Du **aggregierst** die p-Werte zur Signifikanzrate über 932 Firmen, so dass einzelne Annahmenverletzungen sich auswaschen
- Standard-Output von `statsmodels.AutoReg`, kein Zusatz-Setup nötig

### Alternative: Robust Standard Errors (HAC / Newey-West)

Wenn Du heteroskedastische oder autokorrelierte Residuen vermutest, könntest Du Newey-West-Standardfehler verwenden. **Warum bei Dir nicht zwingend nötig:** Du arbeitest auf Differenzen, was die Autokorrelation der Residuen massiv reduziert. Bei der Aggregation über 932 Firmen sind systematische Verzerrungen unwahrscheinlich. Falls der Prof fragt: "Robust-Standardfehler wären eine Option für Einzelfirmen-Inferenz; meine Aussagen beziehen sich auf Querschnittsmediane, nicht auf Einzelfirmen."

### Anwendung bei Dir

- Direkt in Tab. 4.10 (Beispielfirmen Walmart/Boeing/MSFT/Amazon) für Einzelfirmen-p-Werte
- Aggregiert in Tab. 4.1, 4.3c als **Signifikanzrate** (Anteil mit p < 0,05)

---

## 2. Spearman-Rangkorrelation

### Was sie testet

H₀: Es gibt keinen monotonen Zusammenhang zwischen X und Y (ρ = 0)
H₁: Es gibt einen monotonen Zusammenhang (ρ ≠ 0)

### Wie sie rechnet

1. Wandle alle Werte in **Ränge** um (kleinster Wert → Rang 1, ..., größter → Rang n)
2. Berechne die Pearson-Korrelation der Ränge:

> ρ = 1 − (6 · Σ d_i²) / (n · (n² − 1)),  mit d_i = Rang(x_i) − Rang(y_i)

(Die Formel gilt für ranggebundene Daten ohne Ties.)

### Annahmen

- Daten sind mindestens **ordinal** skaliert
- Beobachtungen sind unabhängig
- **Keine** Annahme über Verteilungsform oder linearen Zusammenhang

### Warum bei Dir Spearman statt Pearson

| Aspekt | Pearson | Spearman | Deine Situation |
|---|---|---|---|
| Misst | linearen Zusammenhang | monotonen Zusammenhang | nichtlineare Kopplung möglich |
| Verteilungs-Annahme | bivariate Normalität | keine | σ-Werte sind rechtsschief |
| Ausreißer-Sensitivität | hoch | niedrig (Ränge dämpfen) | einzelne Firmen mit σ > 3 |
| Bei monotoner Trafo | ändert sich | invariant | Du transformierst nicht, aber σ und φ₁ haben sehr unterschiedliche Skalen |

**Der entscheidende Punkt:** Pearson würde Dir bei Real Estate (FCF-σ = 0,60, ROA-σ = 0,011) und Walmart (φ₁ = −0,69) automatisch verzerrte Korrelationen geben, weil die Extremfirmen die Pearson-Berechnung dominieren. Spearman ranged die Werte und gleicht das aus.

### Alternative: Kendall's τ

Auch nicht-parametrisch, sehr ähnlich. Vorteile: noch robuster gegen Ausreißer, statistisch besser interpretierbar bei kleinen Stichproben. Nachteile: rechenintensiver, weniger verbreitet, in der finanzwissenschaftlichen Literatur unüblich. **Für n = 932 sind Spearman und Kendall praktisch äquivalent.** Spearman ist die Standardwahl in Deinem Forschungsfeld.

### Anwendung bei Dir

- **Tab. 4.7:** φ₁ × σ(ΔY) pro Kennzahl, n je Kennzahl ≈ 932
- Werte: ROA −0,089 (p = 0,006), EBIT-Marge −0,182 (p < 0,001), D/E −0,241 (p < 0,001)
- **In Kap. 6 (FF3):** Spearman ersetzt das alte Cramér's V für Quadrantenüberschneidungen (Prof-Entscheidung 26.03.2026)

### Interpretation Deiner Werte

Mit Rucker et al. (2015) als methodischer Anker:

| |ρ| | Klassifikation | Konsequenz für Median-Split |
|---|---|---|
| < 0,3 | schwach | Median-Split methodisch unproblematisch |
| 0,3–0,5 | moderat | Vorsicht, Einschränkung erwähnen |
| > 0,5 | stark | Median-Split nicht zulässig, eindimensional auswerten |

**Deine Werte alle < 0,25** → Trennbarkeit grundsätzlich gegeben, Bilanzstruktur mit Vorbehalt.

### Wichtig: Statistische Signifikanz vs. praktische Bedeutung

Bei n = 932 sind selbst |ρ| = 0,09 statistisch signifikant (p = 0,006 für ROA). Das heißt: **statistische Signifikanz ist hier kein Maß für Stärke**, nur Indikator für "ungleich null". Die *Effektstärke* misst Du über den absoluten ρ-Wert. Diese Unterscheidung gehört in jede Diskussion großer Stichproben.

---

## 3. χ²-Test auf Gleichverteilung

### Was er testet

H₀: Die k Kategorien sind gleichmäßig besetzt (Erwartungswert n/k pro Zelle)
H₁: Mindestens eine Kategorie weicht systematisch ab

### Wie er rechnet

> χ² = Σ_{i=1}^{k} (O_i − E_i)² / E_i

mit O_i = beobachtete Häufigkeit, E_i = erwartete Häufigkeit unter H₀.

Unter H₀ folgt χ² einer χ²-Verteilung mit (k−1) Freiheitsgraden — bei Dir k = 4 Quadranten, also 3 Freiheitsgrade.

### Annahmen

1. **Unabhängige** Beobachtungen (jede Firma fällt in genau einen Quadranten)
2. Erwartete Häufigkeit pro Zelle **mindestens 5** (besser ≥ 10)
3. Kategorien sind eindeutig definiert (keine Überschneidung)

### Warum er bei Dir gut passt

- Bei n = 931 und k = 4 ist die erwartete Häufigkeit pro Zelle ≈ 233 — Annahme 2 weit übererfüllt
- Quadranten sind durch Median-Split sauber getrennt — Annahme 3 erfüllt
- Du testest hier eine **konkrete Verteilungs-Hypothese** (Gleichverteilung), nicht eine Korrelation — χ² ist die Standardwahl

### Alternative: Fisher's Exact Test

Für kleine Stichproben (n < 30) oder bei einzelnen Zellen mit erwarteter Häufigkeit < 5. **Bei Dir nicht relevant**, weil n riesig.

### Alternative: G-Test (Likelihood-Ratio)

Mathematisch verwandt, asymptotisch äquivalent zu χ². Wird in der Bioinformatik bevorzugt, in der Finanzliteratur ist χ² Standard. **Bei Dir keine praktische Differenz.**

### Anwendung bei Dir

- **Tab. 4.8:** Pro Kennzahl wird geprüft, ob die vier Quadranten gleichmäßig mit ~n/4 besetzt sind
- **Befund:** 4 von 7 Kennzahlen unauffällig (ROA, ROE, FCF-Marge, EK-Quote — p > 0,05); 3 (EBIT-Marge, Current Ratio, D/E) signifikant abweichend (p < 0,001)
- **Inhalt der Abweichung:** Korrektiv-Volatil und Persistent-Stabil überrepräsentiert (~28–29 %), Korrektiv-Stabil und Persistent-Volatil unterrepräsentiert (~21–22 %) — also Diagonalpaare

### Wichtig: Was Dein χ²-Test NICHT direkt sagt

Der Test sagt: "Die Verteilung ist nicht gleichmäßig." Er sagt **nicht**: "Wie stark ist die Abweichung?" — das ist Aufgabe der Effektstärke (siehe Cramér's V unten).

Bei n = 931 wird selbst eine winzige praktische Abweichung statistisch hochsignifikant. Daher gehört die Effektstärken-Diskussion daneben.

---

## 4. χ²-Test auf Unabhängigkeit (Kontingenztest)

### Was er testet

H₀: Zwei kategoriale Variablen sind unabhängig (z.B. Sektor und Quadrant)
H₁: Es gibt einen Zusammenhang

### Wie er rechnet

Wie der Gleichverteilungs-Test, aber die erwarteten Häufigkeiten ergeben sich aus den Randhäufigkeiten der Kontingenztafel:

> E_{ij} = (Zeilensumme_i × Spaltensumme_j) / Gesamt-n

und die Freiheitsgrade sind (Zeilen − 1) × (Spalten − 1).

### Anwendung bei Dir

- **Kap. 6 (FF3):** Sektor (10 Kategorien) × Quadrant (4 Kategorien) → df = 9 × 3 = 27
- **Bestätigt** den Befund aus Tab. 4.4: Quadrantenverteilung hängt systematisch vom Sektor ab

### Wichtig

Der Unabhängigkeits-χ² ist **strukturell verwandt** mit dem Gleichverteilungs-χ², aber konzeptuell anders: Hier prüfst Du Zusammenhänge zwischen zwei Variablen, dort prüfst Du Verteilung einer Variable. In Deiner FF1 (Tab. 4.8) nutzt Du die Gleichverteilungs-Form; in Kap. 6 die Unabhängigkeits-Form.

---

## 5. Cramér's V — Effektstärke für χ²-Tests

### Was es misst

Die **Stärke** des Zusammenhangs (Effektstärke), nicht nur die Existenz.

### Wie es rechnet

> V = √( χ² / (n · (k − 1)) )

mit k = min(Zeilen, Spalten). Wertebereich 0 (kein Zusammenhang) bis 1 (perfekter Zusammenhang).

### Faustregeln (Cohen 1988, modifiziert für df)

| Cramér's V (df = 3) | Interpretation |
|---|---|
| ≈ 0,06 | klein |
| ≈ 0,17 | mittel |
| ≈ 0,29 | groß |

### Wo bei Dir

- **Kap. 6 (FF3):** Sektor × Quadrant — Cramér's V quantifiziert die Stärke des Brancheneffekts
- **NICHT in Kap. 5 (FF2):** Hier hat Dein Prof am 26.03.2026 entschieden, dass das alte Cramér's V für Quadrantenüberschneidungen durch **Spearman-Rangkorrelation** ersetzt wird. Grund vermutlich: Cramér's V wertet die Quadranten als rein kategorial aus, ohne deren Ordnungsstruktur zu nutzen. Spearman behält die ordinale Information (φ₁-Stärke bleibt geordnet).

### Argument für Verteidigung

Wenn der Prof fragt "Warum ersetzen wir Cramér's V durch Spearman in FF2?" — die Antwort: "Weil Quadranten implizit auf einer ordinalen Achse liegen (mehr/weniger Mean-Reversion, mehr/weniger Volatilität). Cramér's V verwirft diese Ordnung; Spearman nutzt sie. Das macht Spearman bei monotoner Hypothese mächtiger."

---

## 6. Wilcoxon-Vorzeichen-Rang-Test (Wilcoxon Signed-Rank)

### Was er testet

H₀: Die Verteilungen zweier **gepaarter** Stichproben sind gleich (Median der Differenzen = 0)
H₁: Die Verteilungen unterscheiden sich systematisch

### Wie er rechnet

1. Bilde die Differenzen d_i = X_i − Y_i für jede gepaarte Beobachtung
2. Sortiere die |d_i| und vergebe Ränge
3. Bilde die Summe der Ränge mit positivem Vorzeichen (W⁺) und negativem Vorzeichen (W⁻)
4. Die Teststatistik ist min(W⁺, W⁻)

Bei großem n approximiert die Statistik eine Normalverteilung.

### Annahmen

1. **Gepaarte** Beobachtungen (dieselbe Firma in beiden Halbperioden)
2. Symmetrische Verteilung der Differenzen (schwächere Annahme als Normalverteilung)
3. Mindestens ordinale Skalierung der Differenzen

### Warum bei Dir Wilcoxon statt gepaartem t-Test

| Aspekt | gepaarter t-Test | Wilcoxon | Deine Situation |
|---|---|---|---|
| Verteilungsannahme | Normalverteilung der Differenzen | symmetrisch (schwächer) | φ₁-Differenzen wahrscheinlich nicht streng normal |
| Ausreißer-Sensitivität | hoch | niedrig | einzelne Firmen mit dramatischen Regimewechseln möglich |
| Mächtigkeit bei Normalverteilung | leicht höher | ~95 % der t-Test-Mächtigkeit | bei n = 932 spielt das praktisch keine Rolle |
| Standard im Forschungsfeld bei Halbperiodenvergleich | uneinheitlich | etabliert | Wilcoxon ist konservativer und damit defensiver |

### Alternative: Mann-Whitney-U / Wilcoxon-Rangsummentest

Das ist der Test für **unabhängige** Stichproben. **Bei Dir falsch**, weil dieselbe Firma in beiden Halbperioden vorkommt — Beobachtungen sind gepaart, nicht unabhängig.

### Anwendung bei Dir (geplant für 4.5.4)

- Pro Kennzahl: Berechne φ₁_pre und φ₁_post pro Firma
- Bilde die Differenzen d_i = φ₁_post − φ₁_pre
- Wilcoxon prüft: Ist die typische Differenz signifikant von null verschieden?

**Erwarteter Befund:** Profitabilität → keine Verschiebung (strukturelle Marktmechanismen); Kapitalstruktur → ggf. Verschiebung durch Niedrigzins-Regime.

---

## 7. Threshold-AR(1) / Vorzeichen-Split (geplant für 4.5.5)

### Was getestet wird

Ist die Mean-Reversion symmetrisch oder asymmetrisch — d.h. korrigieren positive und negative Schocks gleich schnell?

H₀: φ₁⁺ = φ₁⁻ (symmetrische Korrektur)
H₁: φ₁⁺ ≠ φ₁⁻ (Asymmetrie)

### Wie es rechnet — zwei Varianten

**Variante A: Vorzeichen-Split der Residuen**

1. Schätze AR(1) wie üblich
2. Splitte die Beobachtungen nach Vorzeichen von ε(t−1)
3. Schätze φ₁⁺ und φ₁⁻ separat
4. Teste die Differenz mit z-Test oder Bootstrap

**Variante B: TAR(1)-Modell direkt**

> ΔY(t) = c + φ₁⁺ · ΔY(t−1) · 1[ΔY(t−1) > 0] + φ₁⁻ · ΔY(t−1) · 1[ΔY(t−1) ≤ 0] + ε(t)

Schätze in einer einzigen Regression mit Indikatorvariablen.

### Annahmen

- Wie AR(1) plus: hinreichend Beobachtungen pro Regime (mindestens ~30 pro Vorzeichen)

### Warum überhaupt testen

Die AR(1)-Spezifikation **unterstellt Symmetrie**. Wenn ökonomisch Asymmetrien existieren (z.B. "loss aversion" auf Unternehmensebene, konservative Bilanzpolitik nach negativen Schocks), würde das Hauptmodell diese verschleiern. Der Test ist eine Robustheits-Prüfung.

### Alternative: Asymmetrische GARCH-Modelle (EGARCH, GJR-GARCH)

Diese modellieren Volatilitäts-Asymmetrien. **Bei Dir nicht passend**, weil Du nicht primär die Varianz, sondern die Mittelwerts-Korrektur untersuchst. EGARCH wäre eine sinnvolle Erweiterung für eine andere Forschungsfrage.

### Anwendung bei Dir (geplant)

- Pro Kennzahl wird φ₁⁺ und φ₁⁻ geschätzt
- Visualisierung als Forest-Plot mit Konfidenzintervallen
- Bonferroni-Korrektur über die 7 Kennzahlen-Tests

---

## 8. Bonferroni-Korrektur

### Was sie macht

Korrigiert die Signifikanzschwelle bei multiplen Tests, um die familienweise Fehlerrate (FWER) zu kontrollieren.

> α_korrigiert = α / m

mit m = Anzahl der parallelen Tests.

### Warum sie nötig ist

Bei 20 unabhängigen Tests mit α = 0,05 ist die Wahrscheinlichkeit, mindestens einen falsch-positiven Befund zu sehen, ≈ 64 % (1 − 0,95²⁰). Ohne Korrektur produziert man Pseudo-Befunde.

### Wo bei Dir

- **Kap. 5 Übergang:** Für 42 Paartests in φ₁- und σ-Korrelationsmatrix → α = 0,05 / 42 ≈ 0,0012
- **4.5.5 (geplant):** Für 7 Asymmetrie-Tests → α = 0,05 / 7 ≈ 0,007

### Alternative: Holm-Bonferroni / Benjamini-Hochberg

| Verfahren | Idee | Mächtigkeit | Wann |
|---|---|---|---|
| **Bonferroni** | Strikte Schwellenkorrektur | konservativ | wenn Du wenige, kritische Tests hast und Falsch-Positive vermeiden willst |
| **Holm-Bonferroni** | sequentielle Korrektur | etwas mächtiger | als universelle Verbesserung gegenüber Bonferroni |
| **Benjamini-Hochberg (FDR)** | kontrolliert False-Discovery-Rate statt FWER | deutlich mächtiger | bei vielen Tests in Exploration (z.B. Genomik) |

**Warum Bonferroni für Dich.** In einer Masterarbeit ist Bonferroni die defensive, etablierte Wahl. Wenn Du sagst "Ich nutze Bonferroni", wirft Dir niemand vor, zu liberal zu sein. Holm wäre die elegantere, aber weniger verbreitete Wahl. FDR ist für explorative Genomik üblich, nicht für Hypothesenprüfung in der Finanzökonometrie.

### Wichtig: Effekt der Korrektur

Bei α = 0,05 / 42 ≈ 0,0012 bleiben nur Korrelationen mit p < 0,0012 als "signifikant" stehen. Bei n = 932 sind das immer noch viele — aber der Befund "alle Korrelationen sind nach Bonferroni-Korrektur signifikant" ist deutlich stärker als "alle sind unkorrigiert signifikant".

---

## 9. Test-Auswahllogik (Entscheidungsbaum)

```
Ich will testen, ob...
│
├── ... ein Modell-Koeffizient von null verschieden ist
│       → t-Test (Standard-Output von OLS/AutoReg) [§1]
│
├── ... zwei metrische Variablen miteinander zusammenhängen
│       │
│       ├── linear, normalverteilte Daten
│       │       → Pearson-Korrelation [du nutzt das nicht]
│       │
│       └── monoton, nicht-normal, ausreißerlastig
│               → Spearman-Rangkorrelation [§2]
│
├── ... eine kategoriale Verteilung von einer erwarteten abweicht
│       → χ²-Test auf Gleichverteilung [§3]
│
├── ... zwei kategoriale Variablen unabhängig sind
│       │
│       ├── Existenz prüfen
│       │       → χ²-Test auf Unabhängigkeit [§4]
│       │
│       └── Stärke quantifizieren
│               → Cramér's V [§5]
│               oder bei ordinalen Kategorien: Spearman [§2]
│
├── ... zwei gepaarte Stichproben sich unterscheiden
│       │
│       ├── normalverteilt
│       │       → gepaarter t-Test [du nutzt das nicht]
│       │
│       └── nicht-normal, ausreißerlastig
│               → Wilcoxon-Vorzeichen-Rang-Test [§6]
│
├── ... ein Modell asymmetrisch reagiert
│       → TAR(1) / Vorzeichen-Split [§7]
│
└── ... viele Tests gleichzeitig laufen
        → Bonferroni-Korrektur der Signifikanzschwelle [§8]
```

---

## 10. Was Du bewusst NICHT testest (mit Begründung)

Ein guter Methodikteil zeigt nicht nur, *was* getestet wird, sondern auch *was bewusst weggelassen* wurde. Dein Prof wird mindestens eine dieser Fragen stellen.

### 10.1 Stationaritätstests (ADF, KPSS, PP)

**Was sie wären.** Augmented Dickey-Fuller (ADF), Kwiatkowski-Phillips-Schmidt-Shin (KPSS), Phillips-Perron (PP) — alle testen, ob eine Zeitreihe stationär ist (Mittelwert/Varianz konstant über die Zeit).

**Warum Du sie nicht für jede einzelne Reihe ausführst.**

1. Du erzwingst Stationarität durch erste Differenzen — die Differenzbildung ist eine *Lösung*, kein *Test*
2. Bei T = 100 Quartalen sind ADF-Tests notorisch schwach (geringe Power)
3. Bei 6.521 Schätzungen wäre die Aggregation der p-Werte ein eigenes Forschungsthema

**Verteidigungsantwort.** "Stationarität wird durch die Differenzbildung methodisch hergestellt; die Levels-Spezifikation in 4.5.1 ist die Robustheits-Prüfung gegen die Annahme. Einzelreihen-ADF-Tests bei T = 100 sind statistisch zu schwach, um auf Querschnittsebene aggregierbar zu sein."

### 10.2 Granger-Kausalitäts-Tests

**Was sie wären.** Test, ob die Vergangenheit von X die Zukunft von Y vorhersagen kann (über deren eigene Vergangenheit hinaus).

**Warum nicht in FF1.** Du machst univariate AR(1)-Modelle — eine Reihe, kein Multi-Variablen-System. Granger gehört in FF2 (Lead-Lag-Analyse), wo Du Cross-Ratio-Beziehungen prüfst.

### 10.3 Pearson-Korrelation

Wie in §2 ausgeführt: bei rechtsschiefen σ-Werten und Ausreißern ist Pearson verzerrt. Spearman ist robuster.

### 10.4 Levene's Test / Bartlett's Test (Varianzgleichheit)

**Was sie wären.** Tests, ob mehrere Gruppen gleiche Varianzen haben.

**Warum nicht.** Dich interessiert die Varianz selbst (σ als Quadrantendimension), nicht deren Gleichheit zwischen Gruppen. Wenn Du Varianzunterschiede zwischen Sektoren analysieren wolltest, würdest Du das deskriptiv über die σ-Heatmap machen, nicht über einen Hypothesentest.

### 10.5 ANOVA / Kruskal-Wallis (Mittelwertsvergleich über mehrere Gruppen)

**Was sie wären.** ANOVA testet, ob die Mittelwerte mehrerer Gruppen gleich sind (parametrisch). Kruskal-Wallis ist die nicht-parametrische Variante.

**Warum nicht.** Du vergleichst nicht *die* Mittelwerte über Sektoren, sondern beschreibst *Verteilungen*. Ein ANOVA-p-Wert würde Dir bei n = 932 immer signifikant ausschlagen, ohne ökonomisch interessant zu sein. Du löst das eleganter über deskriptive Heatmaps + Sektor-Profile.

---

## Schnellreferenz für Verteidigung

| Wenn der Prof fragt... | Antworte ungefähr... |
|---|---|
| Warum Spearman, nicht Pearson? | Rechtsschiefe σ-Verteilungen, ausreißerresistent, ordinaler Charakter der Daten. Bei n = 932 ist Pearson nicht robuster, nur empfindlicher. |
| Warum keine Stationaritätstests? | Stationarität wird durch Differenzbildung hergestellt; Levels-Vergleich in 4.5.1 ist die strukturelle Robustheits-Prüfung. ADF bei T = 100 zu schwach. |
| Warum Wilcoxon statt t-Test in 4.5.4? | Differenzen wahrscheinlich nicht streng normal, ausreißerresistent, konservativer und damit defensiver. |
| Warum χ² auf Gleichverteilung statt Korrelations-Test? | Frage ist nicht "hängen die Quadranten zusammen", sondern "sind sie gleich besetzt" — andere Hypothesen-Klasse. |
| Warum Cramér's V in FF3, aber nicht in FF2? | FF2-Quadranten haben ordinale Information, die Spearman nutzt; Cramér's V verwirft sie. FF3 testet kategoriale Sektor-Quadrant-Kontingenz, da ist Cramér's V passend. |
| Warum Bonferroni und nicht FDR? | Defensive, etablierte Wahl in der Finanzökonometrie. FDR ist für explorative Genomik üblich. |
| Bei n = 932 ist doch alles signifikant? | Ja — deshalb berichte ich Effektstärken (|ρ|, Cramér's V) parallel zur Signifikanz. Die Signifikanz zeigt nur "ungleich null", die Effektstärke "wie stark". |
| Warum nicht ANOVA über Sektoren? | Bei n = 932 schlägt jeder ANOVA-p-Wert signifikant aus, ohne ökonomische Aussage. Deskriptive Heatmaps + Sektor-Profile sind interpretativ stärker. |

---

## Argumentations-Architektur Deiner Tests

Dein Test-Bouquet hat eine klare Erzähllogik, die Du in der Verteidigung sichtbar machen solltest:

1. **t-Test auf φ₁** beweist auf Einzelfirmen-Ebene, dass das AR(1)-Signal real ist
2. **Aggregierte Sig.-Rate** zeigt, dass das Signal über das Panel verteilt ist
3. **Spearman φ₁ × σ** prüft die methodische Voraussetzung der Quadrantenklassifikation
4. **χ² auf Gleichverteilung** liefert die zweite Bestätigung der Trennbarkeit
5. **Wilcoxon Halbperiode** prüft die zeitliche Stabilität der Hierarchie
6. **TAR(1) Asymmetrie** prüft die Symmetrie-Annahme des Hauptmodells
7. **Bonferroni** sichert das Ganze gegen Multiple-Testing-Inflation

Jeder Test hat eine konkrete Funktion in der Argumentationskette. Wenn ein Test wegfällt oder hinzukommt, wird ein Glied der Kette schwächer oder stärker — das ist die Logik, mit der Du das Methodendesign verteidigen kannst.
