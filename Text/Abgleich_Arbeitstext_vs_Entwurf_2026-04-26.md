# Abgleich Arbeitstext ↔ Kapitel 4 FF1 (Entwurf)

**Stand:** 26.04.2026
**Verglichen:** `Arbeitstext.docx` (FF1-Notizen, ca. Z. 1416–2280) ↔ `Kapitel_4_FF1_Ergebnisse_Entwurf.docx`
**Legende:** ✅ vollständig umgesetzt · 🟡 teilweise / mit Einschränkung · ❌ fehlt im Entwurf

---

## Gesamteindruck

Die in den Notizen geplante Gliederung ist im Entwurf **vollständig erhalten** (4.1 → 4.5, 4.5 am Ende). Der Hauptbefund — die Drei-Schichten-/Drei-Dynamiktypen-Hierarchie — ist tragend und durchgängig durchgezogen. Auffällige terminologische Verschiebung: „Drei-Schichten-Hierarchie" aus den Notizen heißt im Entwurf „Drei Dynamiktypen". Inhaltlich identisch.

Quantitativ:
- Vom Arbeitstext geplante 4.1–4.4 ≈ 90 % ausformuliert.
- 4.5 Robustheit zu ca. 60 % umgesetzt: 4.5.1, 4.5.2, 4.5.3 fertig — 4.5.4 (Halbperiode) und 4.5.5 (Asymmetrie) sind nur als Platzhalter mit Methoden-Skizze drin.
- 6 als „**VERTIEFUNG**" markierte Literaturanker im Text sind als Marker stehengeblieben und noch nicht ausformuliert.
- Eine geplante Sektor-Streuungs-Grafik (φ₁-Std je Sektor × Kennzahl) fehlt komplett.

---

## 4.1 Analyse nach Kennzahl

### 4.1.1 Überblick der Drei-Schichten / Drei Dynamiktypen

| Notiz im Arbeitstext | Status | Bemerkung |
|---|---|---|
| Tab. 4.1 mit Median φ₁, Sig.%, Median σ, Half-Life | ✅ | Tab. 4.1 im Entwurf erweitert |
| ℹ️ "Info fehlt": Mittelwert φ₁, Streuung φ₁, Mittelwert σ, **Streuung σ** | ✅ | Alle vier Spalten sind in Tab. 4.1 ergänzt (φ₁ Ø, φ₁ Md, φ₁ σ, σ(ΔY) Ø, σ(ΔY) Md, σ(ΔY) σ). Sehr saubere Umsetzung. |
| t½-Umrechnung in Jahre (E5.4-Notiz) | ✅ | Tab. 4.1 hat zwei Spalten **t½ Q** und **t½ J** — und der Fließtext nutzt beide Skalen ("1,1 bis 1,3 Quartale, also rund einem Drittel Jahr"). Genau wie in der Beispielformulierung der Notiz. |
| 📊 "Grafik fehlt": Histogramm/KDE der φ₁-Verteilung pro Kennzahl | ✅ | Abb. 4.1b: KDE der φ₁-Verteilung mit Histogramm-Hintergrund und Median-/Null-Linien — exakt wie gefordert. |
| 📊 "Grafik fehlt": Histogramm/KDE der σ-Verteilung pro Kennzahl | ✅ | Abb. 4.2b: KDE σ(ΔY), 99-Perzentil-Cutoff. Umgesetzt. |
| Notiz: vor der Hierarchie zuerst Modellgüte über alle 6.521 Schätzungen (R²-Verteilung als Histogramm, Sig.-Rate) deskriptiv | 🟡 | Sig.-Rate ist in Tab. 4.1 enthalten, R²-Verteilung wird in Abb. 4.2 (rechts) gezeigt. Das ist allerdings **nach** der Tabellen-Einführung der Hierarchie und nicht als eigenständiger "Modellgüte-Überblick"-Block. Wenn Du die in der Notiz vorgeschlagene Reihenfolge ernst meinst, müsstest Du den ersten Absatz unter 4.1.1 umstellen: erst R²/Sig. global, dann Hierarchie. Aktuell ist es aber inhaltlich abgedeckt. |
| 5-Punkt-Workflow (Wert → Aussage → BWL → Zusammenhang → Erkenntnis) | 🟡 | Implizit im Fließtext umgesetzt, aber **nicht sichtbar als 5-Punkt-Struktur** mit Markern/Absätzen. Wenn der Workflow Prof-Vorgabe ist, müsstest Du das ggf. nachträglich gliederungstechnisch sichtbar machen — sonst ist der Punkt inhaltlich erfüllt. |
| **VERTIEFUNG #1 — Dichev & Tang (2009): Levels-φ₁ ≈ 0,62 vs. eigene Differenzen-φ₁ = −0,43** | ❌ | Marker steht im Entwurf (Z. 82), Inhalt fehlt. Konkrete Zahlen-Gegenüberstellung mit Methodikerklärung muss noch geschrieben werden. Reihenfolge im Argument: Levels-Persistenz-Befund vs. Veränderungs-Korrektur-Befund — kein Widerspruch, sondern komplementäre Sichten. |

### 4.1.2 Profitabilitätsschicht / Profitabilitätsgruppe

| Notiz | Status | Bemerkung |
|---|---|---|
| Vier Unterabschnitte (ROA, ROE, EBIT-Marge, FCF-Marge) | ✅ | Alle vier mit eigenem Tabellenblock (Tab. 4.2a–4.2d) und Fließtext drin. |
| ROE — Leverage-Verstärkung erklären (ROE = ROA × (1+D/E)) | ✅ | Algebraische Hebel-Logik im Text vorhanden, σ-Kopplung ROE↔D/E (ρ_σ = 0,82) als Vorgriff auf Kap. 5 angekündigt. Sehr gut. |
| FCF-Marge — stärkste Veränderungskorrektur, Sloan-Verbindung | 🟡 | Stärkste φ₁ ist im Text, Sloan-Logik mit ρ ≈ 0,15–0,20 für FCF↔Earnings-Quartettkorrelation ist angedeutet (Verweis auf Dechow 1994). |
| **Abb. 4.4** im Arbeitstext: φ₁-σ-Raum-Verortung pro Kennzahl mit Quadranten-Farbkodierung und Beispielfirmen (NVIDIA, Microsoft, Boeing, Walmart) | 🟡 | **Position verschoben:** Im Entwurf nicht in 4.1.2, sondern in 4.3.3 als Abb. 4.10 (Beispielfirmen-Zeitreihen) + Tab. 4.10. NVIDIA durch **Amazon** ersetzt (vermutlich besser für Persistent-Volatil). Inhalt vorhanden, Verortung anders. Einzige offene Frage: Soll die *Streudiagramm-Darstellung* (alle 932 Firmen im φ₁-σ-Raum, eingefärbt nach Quadrant) zusätzlich zu den Beispielen eigen erscheinen? Das wäre Abb. 4.4 aus den Notizen. Im Entwurf erscheint sie als Abb. 4.9 unter 4.5.3 — **also ist auch das umgesetzt**, nur an anderer Stelle. |
| **Abb. 4.5** Arbeitstext: Zeitreihen-Beispiele 2×2-Panel (NVIDIA, MSFT, BA, WMT, gleich skaliert −2σ bis +2σ) | ✅ | Im Entwurf als Abb. 4.10 unter 4.3.3 vorhanden, mit Walmart, Boeing, Microsoft, Amazon (NVIDIA → Amazon). Inhalt gewahrt. |
| **VERTIEFUNG #2 — Sloan (1996) + Eigenbeobachtung FCF-Sig.rate 96,6 % > 90 %** | ❌ | Marker (Z. 304) steht — Auflösung Sloan-Cashflow-Persistence vs. eigene FCF-Mean-Reversion fehlt. Eigenständiger Argumentationsbaustein, der gut zu Deinem "Mehrfach-Verankerung"-Stil passen würde. |

### 4.1.3 Liquiditätsschicht / Liquiditätsgruppe

| Notiz | Status | Bemerkung |
|---|---|---|
| Current Ratio als Übergangszone (φ₁ ≈ −0,17, Sig. ≈ 60 % im Notiz-Text, real 45,6 %) | ✅ | Als Tab. 4.2e + Fließtext umgesetzt. Übergangscharakter, schwacher Marktmechanismus, Hinweis auf Real-Estate-Anomalie alle drin. |
| 5-Punkt-Workflow (Working-Capital-Zielspanne 1,5–2,0; sektorale Variation) | 🟡 | Inhaltlich abgedeckt, aber nicht als sichtbare 5-Punkt-Struktur. Konkrete Zielwert-Range „1,5–2,0" aus den Notizen ist im Entwurf-Text nicht explizit genannt. |
| **VERTIEFUNG #3 — Eljelly (2004) Liquiditäts-Profitabilitäts-Trade-off** | ❌ | Marker (Z. 362). Hinweis aus Notizen, dass Eljelly im Quellenkanon vorhanden ist und sektorale Heterogenität dokumentiert — wartet auf 1–2 Sätze hier und Detail in 4.3.2 (REIT-Spezialliteratur). |

### 4.1.4 Kapitalstrukturschicht / Kapitalstrukturgruppe

| Notiz | Status | Bemerkung |
|---|---|---|
| D/E und EK-Quote — kein AR-Signal auf Differenzen | ✅ | Tab. 4.2f und 4.2g + Fließtext mit Nullbefund-Argumentation und Verweis auf Levels-Lesart aus 4.5.1. |
| 5-Punkt-Workflow (kein statistisches Rauschen, sondern strategische Natur) | 🟡 | Implizit umgesetzt, kein Workflow-Marker. |
| **VERTIEFUNG #4 — Strebulaev (2007) / Lemmon, Roberts, Zender (2008): Halblebensdauer 6–10 Jahre matcht eigene 4,3 Jahre EK-Quote**; eigene Beobachtung Momentum-Quartil | ❌ | Marker (Z. 426). Sehr starker Argument-Hebel — die Lemmon-et-al.-Halbwertszeit deckt Deine 17-Quartale-Halbwertszeit fast perfekt ab. **Diese Vertiefung ist eine der wirkungsvollsten und sollte priorisiert werden.** |

---

## 4.2 Analyse nach Branche

### 4.2.1 Sektorale Übersicht der AR(1)-Kenngrößen

| Notiz | Status | Bemerkung |
|---|---|---|
| Heatmap φ₁ Sektor × Kennzahl (Abb. 4.6 Notiz → Abb. 4.5 Entwurf) | ✅ | Tab. 4.3 + Heatmap umgesetzt; drei Beobachtungen schön ausformuliert (Hierarchie sektorinvariant, Spreizung Profitabilität, größere Variation Liq./Kap.). |
| Heatmap σ (Abb. 4.7 Notiz → Abb. 4.7 Entwurf) | ✅ | Tab. 4.3b + Heatmap. |
| Heatmap Sig.rate (Abb. 4.8 → Abb. 4.8) | ✅ | Tab. 4.3c + Heatmap. |
| 📊 **"Grafik fehlt": Streuungs-Darstellung pro Sektor × Kennzahl** (φ₁-Std-Heatmap oder Boxplot-Grid Sektor×Kennzahl oder „mean ± std" pro Zelle) | ❌ | **Nicht umgesetzt.** Die drei vorhandenen Heatmaps sind alle Lagemaße. Die geplante vierte Heatmap mit der Streuung pro Sektor × Kennzahl fehlt komplett. Damit fehlt der deskriptiv-statistische Beleg, ob ein Sektor-Median „enge Verteilung" oder „weite Verteilung" hat. Wäre auch in der Diskussion mit dem Prof verteidigbar (E15-Kriterium). |
| Sektor-Profile (10 Sektoren) | ✅ | Sehr ausführlich umgesetzt: Industrials, Consumer Cyclical, Technology, Healthcare, Utilities, Consumer Defensive, Basic Materials, Real Estate, Energy, Communication Services. Jeweils mit Quadranten-Anteilen und Geschäftsmodell-Bezug. **Stärker als der Notizen-Vorschlag.** |
| 5-Punkt-Workflow Sektorebene | 🟡 | Implizit über die Sektor-Profile abgedeckt. |
| Hinweis auf Variable Stichproben/Survivorship Bias an dieser Stelle (kopierte Notiz aus 4.4.x) | 🟡 | Im Entwurf wird das richtigerweise in 4.5.2 statt 4.2.1 ausgewertet — die kopierte Notiz war eine Verschiebe-Markierung, kein eigener Inhalt für 4.2.1. Sauber gelöst. |

### 4.2.2 Quadrantenverteilung pro Sektor

| Notiz | Status | Bemerkung |
|---|---|---|
| Tab./Abb. Quadrantenverteilung pro Sektor (gestapelt, ROA-Klassifikation) | ✅ | Tab. 4.4 + Abb. 4.6. Schöne Drei-Gruppen-Sortierung (Stabile / Korrektiv-Volatile / Persistent-Volatile). |
| Anhang-Hinweis: 11 sektorspezifische φ₁-Verteilungsplots in `output/plots/sectors/` als Abb. A.x | ❌ | Im Entwurf **kein Anhang-Verweis**. Solltest Du im Endausbau einbauen, sonst gehen die Plots verloren oder es entsteht ein „dangling asset". |

---

## 4.3 Interpretation der Ergebnisse

### 4.3.1 Interpretation der Schichthierarchie / Rangordnung

| Notiz | Status | Bemerkung |
|---|---|---|
| Hauptachse Markt vs. Management (Wettbewerbskräfte → Profitabilität; Trade-off/Pecking-Order → Kapitalstruktur; WCM hybrid → Liquidität) | ✅ | **Vollständig und sehr gut ausformuliert.** Stigler 1963, Fama-French 2000, Myers 1984, Modigliani-Miller 1958 alle eingebaut. |
| Earnings-Persistence-Konsistenz (Sloan 1996, Dichev-Tang 2009, Fairfield-Yohn 2001) | ✅ | Eingearbeitet als Brückenargument zwischen Niveau und Veränderung. |
| Verstärker 1: Halblebensdauer-Skala (1,2 / 3,6 / 7,4 / 17,1 Quartale, Faktor 15) | ✅ | Sauber als eigene Argumentationslinie ausgeführt. |
| Verstärker 2: Stromgrößen vs. Bestandsgrößen | ✅ | Bilanzmechanische Lesart als dritte unabhängige Begründung. |
| Synthese der drei Argumentationswege | ✅ | Mehrfach-Verankerungs-Logik explizit benannt — sehr stark argumentativ. |
| Vorgriff auf vierte technische Achse (Zähler-Nenner-Algebra → Kap. 5) | ✅ | Angekündigt. |
| **VERTIEFUNG #5 — DuPont-Brücke (Christie 1982 / Nissim & Penman 2001) als Synthese-Punkt** | ❌ | Marker (Z. 1021). Argumentstärke: klassische Mean-Reversion-Literatur erklärt φ₁; klassische Bilanzliteratur erklärt σ-Kopplung. Beide treffen sich in Deiner Quadrantenklassifikation. **Das ist ein Setup für Kap. 7 (Diskussion) und sollte hier angekündigt werden.** Aktuell fehlt der Hinweis. |

### 4.3.2 Interpretation der sektoralen Heterogenität

| Notiz | Status | Bemerkung |
|---|---|---|
| Utilities (regulatorisch induzierte Mean-Reversion) | ✅ | Eigener Absatz, regulatorische Eigenkapitalanforderungen herausgearbeitet. |
| Real Estate (REITs, Mietverträge, Ausschüttungspflichten) | ✅ | Vollständig argumentiert. |
| Communication Services (Fixkostenstruktur) | ✅ | Eigener Absatz, n=37-Vorbehalt erwähnt. |
| Basic Materials (Rohstoffpreis-Persistenz) | ✅ | Mit Kupfer-Beispiel. |
| Technology (M&A-getriebene Plateaus) | ✅ | Verbunden mit Basic Materials als persistentes Profil. |
| Energy (Hedging, Cashflow-Volatilität) | 🟡 | In 4.2.1 ausführlich beschrieben, in 4.3.2 nicht erneut interpretierend aufgegriffen. **Kleiner Gap:** Der Notiz-Vorschlag „Financial Services besondere Muster (Leverage-Geschäftsmodell, prozyklische Risikoprofile)" entfällt wegen FS-Ausschluss aus FF1; das ist bewusste Abgrenzung — gehört aber inhaltlich in Kap. 6.4 (Financial-Services-Deep-Dive) und sollte hier mit einem Satz „FS gesondert in 6.4 behandelt" abgegrenzt werden. |
| Healthcare (Kapitalintensität) | 🟡 | In 4.2.1 als Profil drin, in 4.3.2 nicht eigenständig interpretiert. |
| Consumer Defensive (Stabilität, Entschuldungsdynamik) | 🟡 | In 4.2.1 als Profil drin, in 4.3.2 nicht eigenständig interpretiert. |
| Konsistente Mechanismen-Erklärung (Schluss: Hierarchie nicht aufgehoben, nur moduliert) | ✅ | Zusammenfassung am Ende von 4.3.2 vorhanden. |
| **VERTIEFUNG #6 — Eigene Beobachtung sektorale Trennbarkeit σ (Faktor 5–10) vs. φ₁ (Faktor 1,3)** als Vorgriff auf FF3 (Größe ↔ σ, ρ bis −0,53; Größe ↔ φ₁, ρ ≈ 0) | ❌ | Marker (Z. 1151). **Sehr starker eigenständiger Befund**, der die Trennbarkeits-Argumentation aus 4.5.3 und den Übergang zu Kap. 6 verstärkt. Wirkt im Argumentationsbogen weniger „literarisch dazugepackt" und mehr „strukturell tragend". |

### 4.3.3 Interpretation der Quadrantenzugehörigkeit

| Notiz | Status | Bemerkung |
|---|---|---|
| Was bedeutet PERSISTENT-VOLATIL etc. operativ? | ✅ | In den vier Beispielfirmen (Walmart, Boeing, Microsoft, Amazon) konkretisiert + abstrakt erläutert. |
| Quadranten als Brücke zu FF2/FF3 | ✅ | Vorgriff auf Konsistenz-Werte (1,2 % volle Konsistenz vs. 97,6 % Profitabilitäts-Konsistenz) und auf σ↔Größe-Korrelation. |
| Trennbarkeitseinordnung mit Rucker et al. 2015 | ✅ | Ausdrücklich genannt. |

---

## 4.4 Erkenntnisse aus FF1

| Notiz | Status | Bemerkung |
|---|---|---|
| Drei Befunde (Hierarchie, Trennbarkeit, sektorale Heterogenität) | ✅ | Sauber und konzentriert. |
| Hypothesen-Abgleich zu 2.5 (drei Beitragsdimensionen: methodisch, empirisch, typologisch) | ✅ | Ausführlich umgesetzt. Beitragsdimension 3 mit ehrlicher Einschränkung (χ²-Test signifikant für 3 von 7 Kennzahlen). Sehr gut. |
| Übergang zu Kap. 5 (FF2) inkl. Block-Hypothese und Bonferroni-Vorschau | ✅ | Vorhanden. |
| Implizite Forderung: explizite Beantwortung der FF1-Frage in einem Satz | ✅ | Antwort steht: „Finanzkennzahlen zeigen systematische Dynamikunterschiede, die sich in eine ökonomisch interpretierbare Drei Dynamiktypen ordnen, durch zwei trennbare strukturelle Eigenschaften beschrieben werden und sektorübergreifend stabil bleiben." |

---

## 4.5 Robustheit

### 4.5.1 Modellvarianten

| Notiz | Status | Bemerkung |
|---|---|---|
| Tab. 4.2 (Notiz) → Tab. 4.5 (Entwurf): φ₁-Mediane vier Modellvarianten | ✅ | Vollständig. Levels, diff1, AR(2)-diff1, Δ₄Y mit allen sieben Kennzahlen. |
| Modellvergleich-Heatmap | ✅ | Abb. 4.3. |
| Levels-Inversion erklärt (φ₁,levels EK-Quote = 0,93 vs. φ₁,diff = −0,04) | ✅ | Erklärt als komplementäre Lesart. |
| AR(2) verstärkt Hierarchie | ✅ | Beziffert (−0,43 → −0,55, R² 0,18 → 0,29, Sig. 90 → 95–99 %). |
| Δ₄Y bestätigt Hierarchie qualitativ | ✅ | Erläutert. |

### 4.5.2 Stichprobenrobustheit

| Notiz | Status | Bemerkung |
|---|---|---|
| Tab. φ₁-Mediane × Stichprobengröße (100/80/60/40 Quartale) | ✅ | Tab. 4.6 + Abb. 4.4 + Text. |
| Profitabilität < 3 % Abweichung | ✅ | Mit Werten belegt. |
| Bilanzstruktur: 16–40 % relative Abweichung erläutert (kleine Absolute → große Relative) | ✅ | Im Text als „nicht aufgehoben, sondern moduliert" eingeordnet. |
| Schluss: Survivorship Bias für qualitative Einordnung unerheblich | ✅ | Steht. |

### 4.5.3 Empirische Trennbarkeit der Quadrantendimensionen

| Notiz | Status | Bemerkung |
|---|---|---|
| Tab. Spearman φ₁ × σ pro Kennzahl, mit p-Werten | ✅ | Tab. 4.7. Werte stimmen mit Notiz-Material überein (\|ρ\| < 0,19 für Profitabilität, 0,19–0,24 für Bilanzstruktur). |
| χ²-Test auf Gleichverteilung der vier Quadranten | ✅ | Tab. 4.8: 4 von 7 Kennzahlen unauffällig, 3 (EBIT-Marge, Current Ratio, D/E) signifikant abweichend. **Wichtig:** Diese Einschränkung ist ehrlich in 4.4 als Beitragsdimension 3 mitgeführt. |
| Abb. Streudiagramme im φ₁-σ-Raum mit Median-Linien (Notiz: „2. Quadrantenlinie fehlt") | ✅ | Abb. 4.9. Die in der Notiz aufgeschriebene Anmerkung „2. Quadrantenlinie fehlt!!!" ist im Entwurf-Plot nicht mehr sichtbar als offener Punkt — sollte aber in der Original-PNG-Datei verifiziert werden, dass beide Median-Splits eingezeichnet sind. |
| Rucker et al. (2015) als methodischer Anker | ✅ | Genannt. |
| Einschränkung Bilanzstruktur explizit benennen | ✅ | Sowohl in 4.5.3 als auch in 4.4 (Beitragsdimension 3). |

### 4.5.4 Halbperioden-Vergleich (Pre/Post-Finanzkrise)

| Notiz | Status | Bemerkung |
|---|---|---|
| Methodik-Beschreibung | ✅ | Im Entwurf vorhanden (zweigeteilte Schätzung 2000Q1–2012Q4 vs. 2013Q1–2024Q4, Wilcoxon-Test, Boxplots). |
| Tabelle Halbperioden-Vergleich | ❌ | **Fehlt komplett.** Marker im Entwurf: „***[Berechnung folgt — Erweiterung E5.1 noch nicht ausgeführt]***" |
| Boxplot φ₁ × Halbperiode | ❌ | Fehlt. |
| Erkenntnis-Auswertung | ❌ | Fehlt. |

### 4.5.5 Asymmetrie der Mean-Reversion

| Notiz | Status | Bemerkung |
|---|---|---|
| Methodik-Beschreibung (φ₁⁺ vs. φ₁⁻ oder TAR(1)) | ✅ | Im Entwurf vorhanden. |
| Tabelle Asymmetrie-Test (Bonferroni über 7 Tests) | ❌ | **Fehlt komplett.** Marker: „***[Berechnung folgt — Erweiterung E5.3 noch nicht ausgeführt]***" |
| Forest-Plot φ₁⁺ vs. φ₁⁻ | ❌ | Fehlt. |
| Erkenntnis-Auswertung | ❌ | Fehlt. |

---

## Zusammenfassung der offenen Punkte (Priorität)

### Hohe Priorität — argumentativ tragend

1. **VERTIEFUNG #5 — DuPont-Brücke in 4.3.1 ankündigen** (Christie 1982, Nissim & Penman 2001). Liefert das Setup für Kap. 7 und schließt die Argumentationskette: Mean-Reversion-Literatur erklärt φ₁; Bilanzliteratur erklärt σ-Kopplung; Quadrantenklassifikation = Synthese. Ein Absatz reicht.
2. **VERTIEFUNG #4 — Lemmon, Roberts & Zender (2008) in 4.1.4** (Halbwertszeit-Match 6–10 Jahre vs. eigene 17 Quartale = 4,3 Jahre). Quantitative Bestätigung Deines Nullbefunds aus etablierter Literatur.
3. **VERTIEFUNG #6 — eigene Beobachtung sektorale Trennbarkeit σ-Faktor 5–10 vs. φ₁-Faktor 1,3 in 4.3.2/4.4**. Strukturell tragend für FF3-Übergang.
4. **4.5.4 + 4.5.5 — Berechnungen E5.1 und E5.3 ausführen** und mit Tabelle/Plot aufnehmen, oder bewusst aus dem Kapitel rausnehmen. Aktuell stehen sie als Platzhalter — das schwächt 4.5 in der Verteidigung. Entweder ganz oder gar nicht.

### Mittlere Priorität — empirische Vollständigkeit

5. **Vierte Sektor-Heatmap φ₁-Std (oder σ-Std)** zur Streuung pro Sektor × Kennzahl. Aktuell sind in 4.2.1 nur Lagemaße visualisiert. E15-Kriterium des Profs.
6. **VERTIEFUNG #1 — Dichev & Tang (2009)-Zahlenvergleich in 4.1.1**. Levels-φ₁ ≈ 0,62 vs. eigene −0,43. Konkrete Gegenüberstellung statt allgemeinem Verweis.
7. **VERTIEFUNG #2 — Sloan (1996) + FCF-Sig.-Beobachtung in 4.1.2**. Lieber kürzer als gar nicht.
8. **VERTIEFUNG #3 — Eljelly (2004) in 4.1.3**. 1–2 Sätze + Real-Estate-REIT-Spezialliteratur in 4.3.2.

### Niedrige Priorität — Feinschliff

9. **Modellgüte als eigener Eingangs-Block in 4.1.1** (R²-Verteilung über alle 6.521 Schätzungen, Histogramm). Aktuell verstreut über Tab. 4.1 und Abb. 4.2 — Notiz wollte das vorgelagert haben.
10. **5-Punkt-Workflow** sichtbar als Strukturmarker (falls Prof-Vorgabe). Aktuell implizit umgesetzt.
11. **Anhang-Hinweis auf 11 sektorspezifische φ₁-Verteilungsplots** (`output/plots/sectors/`) in 4.2.2 ergänzen.
12. **Ein Satz zu Financial-Services-Ausschluss** in 4.3.2 (Verweis auf 6.4-Deep-Dive), damit der Leser weiß, dass FS bewusst ausgegrenzt ist.
13. **Working-Capital-Zielspanne 1,5–2,0** aus der 4.1.3-Notiz als konkrete Ankerzahl ergänzen, sonst bleibt der „Übergangscharakter" abstrakt.
14. **Healthcare/Consumer-Defensive interpretierende Absätze in 4.3.2** (aktuell nur in 4.2.1 deskriptiv, ohne BWL-Mechanismen-Einordnung). Wenn der Sektorblock vollständig sein soll.

---

## Was an der Gliederung absolut stabil geblieben ist

- 4.1 → 4.2 → 4.3 → 4.4 → 4.5
- Innerhalb 4.1: Hierarchie-Übersicht → Profitabilität → Liquidität → Kapitalstruktur
- Innerhalb 4.2: AR(1)-Kenngrößen → Quadrantenverteilung
- Innerhalb 4.3: Schichthierarchie → Sektorale Heterogenität → Quadrantenzugehörigkeit
- Innerhalb 4.5: Modellvarianten → Stichprobe → Trennbarkeit → Halbperiode → Asymmetrie

Keine strukturellen Verschiebungen. Die einzige inhaltliche Verlagerung sind die Beispielfirmen-Visualisierungen (NVIDIA→Amazon-Beispiel + Quadranten-Streudiagramme), die in den Notizen unter 4.1.2 standen und im Entwurf nach 4.3.3 (Tab. 4.10/Abb. 4.10) und 4.5.3 (Abb. 4.9) gewandert sind. Das ist argumentativ sinnvoll: Beispielfirmen passen besser zur Quadranten-Interpretation, das Streudiagramm besser zur Trennbarkeitsprüfung.
