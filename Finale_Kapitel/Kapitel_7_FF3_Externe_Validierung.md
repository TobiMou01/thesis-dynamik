# 7 Ergebnisse FF3: Externe Validierung der Dynamikprofile

FF3 prüft, ob die Quadrantenklassifikation aus FF1 ökonomisch interpretierbar ist oder ein statistisches Artefakt darstellt. Die Validierung erfolgt über externe, nicht aus dem AR-Modell stammende Merkmale: Branchenzugehörigkeit (7.2), Unternehmensgröße (7.3), K-Means-Clustering als datengetriebener Robustheitscheck (7.4) und eine separate Analyse des Finanzsektors (7.5). Vorab klärt Abschnitt 7.1 eine konzeptuelle Vorfrage: Gibt es überhaupt ein einheitliches Unternehmensprofil, wenn jede Kennzahl eine eigene Quadrantenzuordnung hat?

## 7.1 Das Konsistenzproblem

### Ausgangslage

Ein Unternehmen hat sieben Quadrantenzuordnungen — eine pro Kennzahl. Es ist denkbar, dass ein Unternehmen für den ROA korrektiv-stabil ist, für die Current Ratio aber persistent-volatil. Bevor externe Merkmale mit der Quadrantenzuordnung verknüpft werden können, muss geklärt werden, ob die Klassifikation innerhalb eines Unternehmens überhaupt konsistent ist.

### Konsistenz-Scores

![Abb. 7.1: Konsistenz der Quadrantenzuordnung auf drei Aggregationsebenen. Der Anteil voll konsistenter Unternehmen (alle Kennzahlen im selben Quadranten) steigt von 1,2 % (Gesamt) über 15,6 % (Profitabilität) auf 41,5 % (Kapitalstruktur). Der Anteil mit Mehrheitskonsistenz (≥50 %) erreicht bei schichtbasierter Betrachtung nahezu 100 %.](Kapitel_7_Grafiken/abb_7_3_konsistenz.png)

Tabelle 7.1 zeigt die Konsistenz auf drei Ebenen.

**Tabelle 7.1:** Konsistenz der Quadrantenzuordnung

| Ebene | Mean | Median | Voll konsistent | Mehrheit ($\geq 50\%$) |
|---|---|---|---|---|
| Gesamt (7 Kennzahlen) | 0,557 | 0,571 | 1,2 % | 59,0 % |
| Profitabilität (4 Kennzahlen) | 0,666 | 0,750 | 15,6 % | 97,6 % |
| Kapitalstruktur (2 Kennzahlen) | 0,708 | 0,500 | 41,5 % | 100 % |

Drei Schlussfolgerungen ergeben sich: Erstens sind Quadranten primär kennzahlspezifisch, nicht unternehmensspezifisch — nur 1,2 % aller Unternehmen haben über alle sieben Kennzahlen denselben Quadranten. Zweitens ist die Konsistenz innerhalb der Profitabilitätsschicht hoch: 97,6 % der Unternehmen haben ein konsistentes Mehrheitsprofil über die vier Profitabilitätskennzahlen. Drittens bestätigt dieses Ergebnis den FF2-Befund der schichtinternen Kohärenz — jetzt aus der Unternehmensperspektive statt aus der Korrelationsperspektive.

### Dominante Quadranten

Die Verteilung der dominanten Quadranten (häufigster Quadrant pro Unternehmen über alle sieben Kennzahlen) ist annähernd gleichmäßig: Persistent-Stabil (30,2 %), Korrektiv-Volatil (27,3 %), Korrektiv-Stabil (21,7 %), Persistent-Volatil (20,9 %). Der Median-Split erzeugt also keine extreme Schieflage — die vier Quadranten sind ähnlich groß, mit einer leichten Überrepräsentation stabiler Profile bei reifen Large-Cap-Unternehmen.

## 7.2 Brancheneffekte: $\chi^2$-Tests

### Ergebnisse

Die $\chi^2$-Tests auf Unabhängigkeit (Sektor $\times$ Quadrant) prüfen, ob die Branchenzugehörigkeit die Quadrantenverteilung systematisch beeinflusst. Tabelle 7.2 zeigt die Ergebnisse für alle sieben Kennzahlen, sortiert nach Effektstärke.

**Tabelle 7.2:** $\chi^2$-Tests Sektor $\times$ Quadrant

| Kennzahl | $\chi^2$ | $p$ | Cramér's $V$ | $n$ |
|---|---|---|---|---|
| Current Ratio | 226,8 | $< 0{,}001$ | $0{,}286$ | 925 |
| EBIT-Marge | 221,2 | $< 0{,}001$ | $0{,}282$ | 925 |
| FCF-Marge | 201,9 | $< 0{,}001$ | $0{,}270$ | 925 |
| ROA | 170,4 | $< 0{,}001$ | $0{,}248$ | 924 |
| EK-Quote | 136,2 | $< 0{,}001$ | $0{,}222$ | 925 |
| ROE | 93,5 | $< 0{,}001$ | $0{,}184$ | 924 |
| Debt/Equity | 85,8 | $< 0{,}001$ | $0{,}176$ | 924 |

![Abb. 7.2: Cramér's V für alle sieben Kennzahlen. Alle Effektstärken liegen im Bereich kleiner bis mittlerer Effekte (0,18–0,29). Die stärksten Brancheneffekte zeigen sich bei Current Ratio und EBIT-Marge — Kennzahlen, deren Dynamik stark vom Geschäftsmodell abhängt.](Kapitel_7_Grafiken/abb_7_1_chi2_cramers_v.png)

### Interpretation

Alle sieben Tests sind hochsignifikant ($p < 0{,}001$). Die Effektstärken liegen mit Cramér's $V = 0{,}18$ bis $0{,}29$ im Bereich kleiner bis mittlerer Effekte. Das ist das methodisch relevante Ergebnis: Branche erklärt einen messbaren, aber nicht dominierenden Anteil der Quadrantenzugehörigkeit.

Die stärksten Brancheneffekte zeigen sich bei Current Ratio ($V = 0{,}286$) und EBIT-Marge ($V = 0{,}282$). Beide Kennzahlen sind stark vom Geschäftsmodell abhängig: Liquiditätsmanagement variiert fundamental zwischen kapitalintensiven (Utilities, Real Estate) und kapitalleichten (Technology, Communication Services) Branchen. Die operative Margenstruktur wird durch Fixkostenanteile, Rohstoffabhängigkeit und Regulierung geprägt — allesamt branchenspezifische Merkmale.

Die schwächsten Effekte zeigen Debt-to-Equity ($V = 0{,}176$) und ROE ($V = 0{,}184$). Verschuldungsentscheidungen werden stärker durch unternehmensspezifische Faktoren — Managementphilosophie, Wachstumsstrategie, Kreditwürdigkeit — als durch Branchenzugehörigkeit bestimmt. Der ROE-Effekt ist schwach, weil die mechanische Leverage-Kopplung (vgl. Kapitel 6) unternehmensspezifische Volatilitätseffekte einträgt, die die Branchenvariation überlagern.

Für die ökonomische Relevanz der Klassifikation ist dieser Befund zentral: Wäre $V \approx 1$, wäre die Quadrantenklassifikation redundant zur Branchenklassifikation — sie würde keine zusätzliche Information liefern. Die moderaten $V$-Werte zeigen, dass die Klassifikation über den Brancheneffekt hinaus differenziert und unternehmensspezifische Dynamikmerkmale einfängt.

## 7.3 Größeneffekte

### Die Asymmetrie des Größeneffekts

Die Analyse der Zusammenhänge zwischen Unternehmensgröße und Dynamikparametern ergibt ein asymmetrisches Muster, das die konzeptuelle Trennung der beiden Quadrantendimensionen empirisch bestätigt.

![Abb. 7.3: Größeneffekte auf Volatilität (links) und Korrekturgeschwindigkeit (rechts). Die Mitarbeiterzahl korreliert stark negativ mit σ(ΔY) — größere Unternehmen schwanken weniger. Dagegen zeigt φ₁ keinen konsistenten Zusammenhang mit der Unternehmensgröße. Die beiden Dimensionen der Quadrantenklassifikation haben unterschiedliche externe Treiber.](Kapitel_7_Grafiken/abb_7_2_groesseneffekte.png)

**Befund 1 — Volatilität ist größenabhängig, Korrekturgeschwindigkeit nicht.** Die Mitarbeiterzahl korreliert signifikant negativ mit der Veränderungsvolatilität $\sigma(\Delta Y)$: FCF-Marge ($\rho = -0{,}53$, $p < 0{,}001$), Current Ratio ($\rho = -0{,}53$, $p < 0{,}001$), EBIT-Marge ($\rho = -0{,}41$, $p < 0{,}001$), Eigenkapitalquote ($\rho = -0{,}27$, $p < 0{,}001$), ROA ($\rho = -0{,}19$, $p < 0{,}001$). Größere Unternehmen schwanken weniger — ein Ergebnis, das die Diversifikationshypothese (vgl. Abschnitt 3.2) bestätigt.

Dagegen zeigt die Mitarbeiterzahl keinen konsistenten Zusammenhang mit $\varphi_1$: ROA ($\rho = -0{,}03$, $p = 0{,}34$), ROE ($\rho = -0{,}05$, $p = 0{,}12$), EBIT-Marge ($\rho = -0{,}04$, $p = 0{,}24$). Die Korrekturgeschwindigkeit ist weitgehend größenunabhängig. Ökonomisch bedeutet das: Ob ein Unternehmen 500 oder 50.000 Mitarbeiter hat, beeinflusst die Magnitude der Quartalschwankungen — aber nicht, wie schnell sich Abweichungen korrigieren. Der Korrekturmechanismus (Wettbewerb, Normalisierung von Einmaleffekten) scheint ein marktgetriebener Prozess zu sein, der unabhängig von der Unternehmensgröße wirkt.

**Befund 2 — Operationale Größe dominiert finanzielle Größe.** Die Mitarbeiterzahl ist ein stärkerer Prädiktor für $\sigma$ als die Marktkapitalisierung (Current Ratio: $\rho_{\text{Employees}} = -0{,}53$ vs. $\rho_{\text{MarketCap}} = -0{,}23$). Operationale Diversifikation — mehr Standorte, Produktlinien, Kundensegmente — glättet Quartalsvolatilität effektiver als bloße finanzielle Größe. Fama und French (1992) dokumentieren Größeneffekte auf Renditen; die vorliegende Arbeit erweitert diesen Befund auf die Dynamik der Kennzahlen und zeigt, dass Größe selektiv auf die Volatilitätsdimension wirkt.

**Befund 3 — Debt-to-Equity als Ausnahme.** Debt-to-Equity zeigt keinerlei Größeneffekt — weder auf $\varphi_1$ ($\rho = +0{,}10$) noch auf $\sigma$ ($\rho = -0{,}01$). Die Verschuldungsdynamik ist damit weder von der Branche (schwächster $\chi^2$-Effekt) noch von der Unternehmensgröße abhängig. Sie ist die am stärksten unternehmensspezifische Kennzahl in der gesamten Analyse — ein Befund, der konsistent mit der Theorie diskreter Finanzierungsentscheidungen ist.

## 7.4 K-Means als Robustheitscheck

### Methodik und Ergebnisse

Die K-Means-Clusteranalyse mit $k = 2$ auf den AR-Dynamik-Features ($\varphi_1$ und $\sigma$ für alle sieben Kennzahlen) identifiziert zwei Cluster, die sich primär über die Volatilitätsdimension differenzieren.

![Abb. 7.4: K-Means-Cluster im φ₁-σ-Raum am Beispiel ROA (links) und Debt-to-Equity (rechts). Cluster 0 (blau, n = 751) zeigt niedrige Volatilität, Cluster 1 (rot, n = 180) hohe Volatilität. Die φ₁-Werte sind bei Profitabilität nahezu identisch; bei Debt-to-Equity zeigt Cluster 1 sowohl höhere Volatilität als auch stärkere Mean-Reversion.](Kapitel_7_Grafiken/abb_7_4_kmeans_cluster.png)

**Tabelle 7.3:** K-Means-Cluster-Profile (Mediane)

| Kennzahl | Cluster 0 ($n = 751$, 81 %) $\varphi_1$ / $\sigma$ | Cluster 1 ($n = 180$, 19 %) $\varphi_1$ / $\sigma$ |
|---|---|---|
| ROA | $-0{,}434$ / $0{,}014$ | $-0{,}426$ / $0{,}033$ |
| ROE | $-0{,}436$ / $0{,}038$ | $-0{,}361$ / $0{,}194$ |
| EBIT-Marge | $-0{,}435$ / $0{,}097$ | $-0{,}413$ / $0{,}305$ |
| FCF-Marge | $-0{,}465$ / $0{,}149$ | $-0{,}432$ / $0{,}306$ |
| Current Ratio | $-0{,}179$ / $0{,}299$ | $-0{,}152$ / $0{,}477$ |
| Debt/Equity | $-0{,}067$ / $0{,}140$ | $-0{,}214$ / $2{,}605$ |
| EK-Quote | $-0{,}046$ / $0{,}028$ | $-0{,}011$ / $0{,}058$ |

### Interpretation

**Cluster 0 — Stabiles Mehrheitsprofil (81 %).** Moderate Profitabilitäts-Mean-Reversion, niedrige Volatilität über alle Kennzahlen, Median-Mitarbeiterzahl von 10.616. Dies ist das typische Profil eines reifen, diversifizierten Unternehmens.

**Cluster 1 — Hochvolatile Minderheit (19 %).** Ähnliche $\varphi_1$-Werte bei Profitabilität (Differenz $< 0{,}03$), aber zwei- bis dreifach höhere Volatilität über alle Kennzahlen. Der extremste Unterschied zeigt sich bei Debt-to-Equity: $\sigma = 2{,}605$ in Cluster 1 gegenüber $0{,}140$ in Cluster 0 — ein Faktor von 18. Gleichzeitig zeigt Cluster 1 bei D/E eine stärkere Mean-Reversion ($\varphi_1 = -0{,}214$ vs. $-0{,}067$), was darauf hindeutet, dass diese Unternehmen häufige, aber systematisch korrigierende Refinanzierungsereignisse erleben. Die Median-Mitarbeiterzahl von 5.050 (vs. 10.616 in Cluster 0) bestätigt den Größeneffekt: Kleinere Unternehmen sind in der hochvolatilen Minderheit überrepräsentiert.

### Sektorale Zusammensetzung

Die sektorale Zusammensetzung der Cluster ist konsistent mit den Befunden aus Kapitel 5: Healthcare (37 % in Cluster 1) und Energy (31 %) sind im hochvolatilen Cluster überrepräsentiert, Industrials (11 %) und Utilities (10 %) unterrepräsentiert. Healthcare-Unternehmen unterliegen langen und kostspieligen Produktentwicklungszyklen (Pharma-Pipelines) und regulatorischen Risiken, die hohe Quartalsvolatilität erzeugen. Energieunternehmen sind rohstoffpreisgetrieben.

### Methodische Implikation

K-Means bestätigt die Quadrantenklassifikation aus einer multivariaten Perspektive: Die Hauptdifferenzierung erfolgt über die Volatilitätsachse, nicht über die Persistenzachse. Der Median-Split und K-Means gelangen zur selben qualitativen Aussage — der Median-Split macht sie über zwei separate, interpretierbare Achsen transparent, K-Means fasst sie multivariat zusammen. Dieser Befund adressiert die methodische Kritik am Median-Split (MacCallum et al., 2002; vgl. Abschnitt 2.4): Die Dichotomisierung ist zwar vereinfachend, aber die datengetriebene Alternative bestätigt die Kerndifferenzierung.

## 7.5 Financial Services: Regulatorische Mean-Reversion

### Vergleich mit der Hauptanalyse

Der Finanzsektor wurde in der Hauptanalyse exkludiert, weil regulatorische Rahmenbedingungen (Basel III, Solvency II) die Bilanzdynamik fundamental verändern. Die separate Analyse von 176 Finanzunternehmen (100-Quartale-Filter) bestätigt diese Entscheidung.

![Abb. 7.5: Vergleich der φ₁-Mediane zwischen Hauptanalyse (n = 932) und Financial Services (n = 176). Die Profitabilitätskennzahlen sind nahezu identisch. Current Ratio und Debt-to-Equity zeigen im Finanzsektor dramatisch stärkere Mean-Reversion — ein Effekt regulatorischer Eigenkapital- und Liquiditätsanforderungen.](Kapitel_7_Grafiken/abb_7_5_finserv_vergleich.png)

**Tabelle 7.4:** $\varphi_1$-Mediane: Hauptanalyse vs. Financial Services

| Kennzahl | Hauptanalyse ($n = 932$) | FinServ 100Q ($n = 176$) | Differenz |
|---|---|---|---|
| ROA | $-0{,}43$ | $-0{,}43$ | Identisch |
| ROE | $-0{,}43$ | $-0{,}43$ | Identisch |
| EBIT-Marge | $-0{,}43$ | $-0{,}40$ | Gering |
| FCF-Marge | $-0{,}46$ | $-0{,}54$ | Stärker |
| Current Ratio | $-0{,}17$ | $-0{,}41$ | **Massiv stärker** |
| Debt/Equity | $-0{,}09$ | $-0{,}20$ | **Stark stärker** |
| EK-Quote | $-0{,}04$ | $-0{,}05$ | Gering |

### Interpretation

Das Muster ist eindeutig: Die Profitabilitätsschicht ist sektorunabhängig (ROA und ROE identisch), aber die Liquiditäts- und Kapitalstrukturschicht verschiebt sich dramatisch. Im Finanzsektor verschmilzt die Liquiditätsschicht (Current Ratio: $\varphi_1 = -0{,}41$) praktisch mit der Profitabilitätsschicht. Debt-to-Equity zeigt mit $\varphi_1 = -0{,}20$ mehr als doppelt so starke Mean-Reversion wie in der Hauptanalyse.

Die Erklärung liegt in regulatorischen Eigenkapital- und Liquiditätsanforderungen: Banken und Versicherungen müssen Kapitaladäquanzquoten einhalten. Wenn Kennzahlen vom regulatorischen Zielwert abweichen, wird aktiv gegengesteuert — das erzeugt systematische Mean-Reversion, die bei unregulierten Unternehmen fehlt. Die Drei-Schichten-Hierarchie gilt auch im Finanzsektor (Profitabilität $>$ Liquidität $>$ Kapitalstruktur), aber die Abstände zwischen den Schichten verringern sich. Die Exklusion des Finanzsektors in der Hauptanalyse ist gerechtfertigt, da die Bilanzkennzahlen systematisch andere Dynamiken zeigen.

## 7.6 Zusammenfassung FF3

FF3 fragte: Welche externen Merkmale beeinflussen die Quadrantenzuordnung? Die Ergebnisse liefern vier Hauptbefunde:

Erstens ist die Quadrantenklassifikation **ökonomisch interpretierbar**. Branche beeinflusst die Quadrantenverteilung signifikant ($p < 0{,}001$, Cramér's $V = 0{,}18$ bis $0{,}29$), erklärt sie aber nicht vollständig. Die Klassifikation fängt unternehmensspezifische Dynamikmerkmale ein, die über den Brancheneffekt hinausgehen.

Zweitens haben die **zwei Dimensionen unterschiedliche externe Treiber**. Unternehmensgröße wirkt selektiv auf $\sigma(\Delta Y)$ (bis $\rho = -0{,}53$), nicht auf $\varphi_1$. Die Quadrantenklassifikation nutzt damit tatsächlich zwei empirisch trennbare Informationsdimensionen.

Drittens **bestätigt K-Means die Hauptdifferenzierung**: Die datengetriebene Clusteranalyse identifiziert eine stabile Mehrheit (81 %) und eine hochvolatile Minderheit (19 %), wobei die Differenzierung primär über die Volatilitätsachse erfolgt — konsistent mit den Größeneffekten.

Viertens zeigt der **Finanzsektor regulatorische Mean-Reversion**: Die Profitabilitätsschicht ist sektorübergreifend stabil, die Bilanzstrukturschicht verschiebt sich unter regulatorischem Einfluss. Die Exklusion und separate Behandlung ist gerechtfertigt.

---

*Die Kapitel 5–7 haben die drei Forschungsfragen empirisch beantwortet. Das folgende Kapitel 8 diskutiert die Implikationen, ordnet die Befunde in die Literatur ein und benennt die Limitationen der Analyse.*
