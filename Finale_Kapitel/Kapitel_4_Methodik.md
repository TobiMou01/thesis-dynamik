# 4 Methodik

Die zentrale methodische Entscheidung dieser Arbeit, autoregressive Modelle erster Ordnung auf ersten Differenzen von Finanzkennzahlen zu schätzen, folgt aus der Abwägung zwischen statistischer Optimalität und querschnittlicher Vergleichbarkeit (vgl. Abschnitt 4.2). Die folgenden Abschnitte legen die Datenbasis (4.1), das Kernmodell (4.2), die Quadrantenklassifikation (4.3), das Robustheitsdesign (4.4) und die statistischen Testverfahren (4.5) dar.

## 4.1 Datengrundlage

Die empirische Analyse basiert auf Quartalsdaten US-amerikanischer börsennotierter Unternehmen über einen Zeitraum von 25 Jahren (Q1/2000 bis Q4/2024, 100 Quartale). Die Rohdaten wurden über die EODHD Financial API bezogen, die standardisierte Quartalsberichte (Income Statement, Balance Sheet, Cash Flow Statement) im US-GAAP-Format bereitstellt. Die Datenbasis der API umfasst den S&P Composite 1500 Index, der Large-Cap- (S&P 500), Mid-Cap- (S&P 400) und Small-Cap-Unternehmen (S&P 600) vereint und damit ein breites Spektrum der US-amerikanischen Börsenlandschaft abdeckt. Nach Anwendung der in den folgenden Abschnitten beschriebenen Filterkette verbleiben 932 Unternehmen in der finalen Stichprobe.

### Filterkette

Die Stichprobe durchläuft eine vierstufige Filterkette, die in Tabelle 4.1 dokumentiert und in Abbildung 4.1 visualisiert ist.

![Abb. 4.1: Filterkette der Stichprobenkonstruktion. Von 5.871 Unternehmen verbleiben nach vier Filterschritten 932 in der finalen Stichprobe.](Kapitel_4_Grafiken/abb_4_2_filterkette.png)

**Tabelle 4.1:** Filterkette der Stichprobenkonstruktion

| Schritt | Aktion | Vorher | Entfernt | Nachher | Begründung |
|:---:|---|:---:|:---:|:---:|---|
| 1 | API-Datenbasis (Schnittmenge BS/IS/CF) | — | — | 5.871 | Nur Unternehmen mit allen drei Abschlussbestandteilen |
| 2a | Sektor-Filter (Financial Services) | 5.871 | 883 | 4.988 | Regulierte Bilanzen verzerren Kennzahlenvergleichbarkeit |
| 2b | ADR-Filter | 4.988 | 646 | 4.342 | Ausschluss ausländischer Unternehmen (IFRS-Risiko, Doppellistungen) |
| 3 | Vollständigkeitsfilter (100 Quartale) | 4.342 | 3.366 | 976 | Mindestlänge für stabile AR(1)-Schätzung |
| 4 | NaN/Qualitätsfilter | 976 | 44 | 932 | Fehlende Werte und Datenqualitätsprobleme |

Der Ausschluss des Finanzsektors (Schritt 2a) ist eine Standardentscheidung in der empirischen Kennzahlenforschung. Finanzinstitute unterliegen regulatorischen Eigenkapitalanforderungen (etwa Basel III; vgl. IMF, 2017), die ihre Bilanzstruktur-Kennzahlen fundamental von denen unregulierter Unternehmen unterscheiden. Die Current Ratio eines Industrieunternehmens und einer Bank messen konzeptuell verschiedene Dinge, da Letztere durch Mindestliquiditätsquoten regulatorisch gebunden ist. Eine separate Analyse des Finanzsektors wird in Kapitel 7 als Robustheitscheck durchgeführt.

Der ADR-Filter (Schritt 2b) entfernt ausländische Unternehmen, die über American Depositary Receipts an US-Börsen gehandelt werden. Diese berichten häufig nach IFRS statt US-GAAP, was die Vergleichbarkeit der Kennzahlen — insbesondere bei der Umsatzrealisierung (ASC 606 vs. IFRS 15) und der Leasingbilanzierung (ASC 842 vs. IFRS 16) — beeinträchtigt. Zusätzlich werden mögliche Doppellistungen so ausgeschlossen. Sämtliche Unternehmen in der finalen Stichprobe berichten damit nach US-GAAP, sodass Unterschiede in den Kennzahlen-Dynamiken nicht durch abweichende Bilanzierungsregeln verzerrt werden. [TODO: Feedback Prof. Steglich zu USGAAP vs. IFRS einarbeiten, sobald verfügbar.]

### Survivorship Bias

Der Vollständigkeitsfilter (Schritt 3) entfernt 77 % der Unternehmen und erzeugt damit einen substanziellen Survivorship Bias: Die verbleibenden 932 Unternehmen sind seit Q1/2000 ununterbrochen börsennotiert und berichtspflichtig. Unternehmen, die nach 2000 gegründet, gelistet, delistet, fusioniert oder insolvent wurden, sind somit nicht enthalten.

Dieser Bias ist methodisch unvermeidbar für Panelanalysen, die vollständige Zeitreihen voraussetzen, wird jedoch durch eine Robustheitsanalyse mit reduzierten Vollständigkeitsschwellen adressiert (vgl. Abschnitt 4.4): Bei 80 Quartalen umfasst die Stichprobe 1.231, bei 60 Quartalen 1.855 und bei 40 Quartalen 2.356 Unternehmen. Die $\varphi_1$-Mediane für Profitabilitätskennzahlen und die Current Ratio bleiben dabei mit Abweichungen unter 3 % stabil. Kapitalstruktur-Kennzahlen zeigen bei absolut niedrigen $\varphi_1$-Werten relativ größere Schwankungen, ohne dass sich die qualitative Einordnung — schwache Mean-Reversion nahe null — ändert. Die Kernbefunde sind somit kein Artefakt der Stichprobenselektion (vgl. Abschnitt 5.5 für die detaillierten Ergebnisse).

### Datenaufbereitung und Outlier-Behandlung

Die sieben Finanzkennzahlen werden direkt aus den Quartalsberichten berechnet: ROA (Nettoergebnis/Bilanzsumme), ROE (Nettoergebnis/Eigenkapital), EBIT-Marge (EBIT/Umsatz), FCF-Marge (Free Cashflow/Umsatz), Current Ratio (Umlaufvermögen/kurzfristige Verbindlichkeiten), Debt-to-Equity (Fremdkapital/Eigenkapital) und Eigenkapitalquote (Eigenkapital/Bilanzsumme).

Die Ausreißerbehandlung erfolgt in zwei Stufen, wobei die erste auf Rohwerten und die zweite auf den daraus berechneten Kennzahlen operiert. Zunächst identifiziert ein rollierender Fensterfilter (Fenstergröße 8 Quartale) kontextabhängig unplausible Einzelwerte in den Bilanzpositionen, etwa wenn ein Nettoergebnis in einem Quartal isoliert um ein Vielfaches vom umgebenden Niveau abweicht. Ein Wert wird nur dann korrigiert, wenn er von mindestens drei überlappenden Fenstern als Ausreißer identifiziert wird, der Abweichungsfaktor zum Korrekturwert mindestens 5 beträgt und eine Stichprobenprüfung das Ereignis nicht als reales Geschäftsereignis bestätigt hat. Korrigierte Werte werden durch den Median der umgebenden Fenster-Mediane ersetzt. Anschließend werden die aus den bereinigten Rohwerten berechneten Kennzahlen querschnittlich auf dem 1. und 99. Perzentil winsorisiert, um Extremratios durch nahe-Null-Nenner zu begrenzen.

Die Wahl der Winsorisierung auf dem 1./99.-Perzentil folgt der Standardpraxis in der Accounting-Forschung (Leone, Minutti-Meza & Wasley, 2019). Adams, Hayunga und Mansi (2019) weisen darauf hin, dass univariate Winsorisierung allein einflussreiche Beobachtungen nicht vollständig adressiert — insbesondere dann, wenn die Extremwerte nicht am Rand der univariaten Verteilung, sondern im multivariaten Raum liegen. Diesem Einwand trägt der vorgeschaltete rollierende Fensterfilter Rechnung, der kontextsensitiv auf Einzelzeitreihen arbeitet und nicht nur globale Verteilungsgrenzen anlegt.

Kennzahlen mit Nulldivisor (negatives oder verschwindendes Eigenkapital bei ROE und Debt-to-Equity) werden als fehlend klassifiziert. Im abschließenden Qualitätsfilter (Schritt 4) werden Unternehmen entfernt, bei denen eine Zähler- oder Nenner-Spalte mehr als 10 % fehlende Quartale aufweist. Für Nenner-Spalten zählen dabei sowohl fehlende Werte als auch Nullwerte als problematisch, da beide eine undefinierte Kennzahl erzeugen; für Zähler-Spalten zählt nur ein fehlender Wert, da ein Zähler von null ökonomisch valide ist. Das resultierende Panel umfasst 932 Unternehmen mit je 100 Quartalswerten für sieben Kennzahlen.

## 4.2 Modellspezifikation: AR(1) auf ersten Differenzen

Die zentrale Forschungsfrage FF1 fragt nach systematischen Unterschieden in der quartalsweisen Veränderungsdynamik von Finanzkennzahlen. Diese Formulierung legt bereits die abhängige Variable nahe: Nicht das Niveau einer Kennzahl, sondern deren Veränderung von Quartal zu Quartal steht im Fokus. Die folgenden Schritte beschreiben die Modellspezifikation; die Begründung der Modellwahl und das Robustheitsdesign folgen in Abschnitt 4.4.

### Schritt 1: Erste Differenzen als Transformation

Für jedes Unternehmen $i$ und jede Kennzahl $k$ wird die erste Differenz gebildet:

$$\Delta Y_{ik}(t) = Y_{ik}(t) - Y_{ik}(t-1)$$

wobei $Y_{ik}(t)$ den Wert der Kennzahl $k$ für Unternehmen $i$ im Quartal $t$ bezeichnet. Diese Transformation hat drei Vorteile. Erstens hat $\Delta Y$ eine direkte ökonomische Interpretation: Der ROA eines Unternehmens hat sich in diesem Quartal um $x$ Prozentpunkte verändert. Zweitens fördert die Differenzenbildung Stationarität, ohne Annahmen über die Integrationsordnung der Niveaus treffen zu müssen — eine relevante Eigenschaft, da insbesondere Kapitalstruktur-Kennzahlen potenziell einheitswurzelnah sind, eine Integrationsordnung von $I(2)$ oder höher für Finanzkennzahlen jedoch ökonomisch nicht plausibel ist. Drittens argumentieren Fairfield und Yohn (2001), dass Veränderungen in Profitabilitätskomponenten informativer für die Prognose zukünftiger Profitabilität sind als deren Niveaus — ein Befund, der die Wahl der Differenzenanalyse auch inhaltlich stützt.

Eine Einschränkung der ersten Differenzen besteht darin, dass saisonale Muster in Quartalskennzahlen (etwa höhere Q4-Umsätze im Einzelhandel) nicht eliminiert werden. Dieser Aspekt wird über saisonale Differenzen ($\Delta_4 Y$) als Robustheitscheck adressiert (vgl. Abschnitt 4.4).

### Schritt 2: Das AR(1)-Modell

Auf die differenzierten Zeitreihen wird ein autoregressives Modell erster Ordnung geschätzt:

$$\Delta Y_{ik}(t) = c_{ik} + \varphi_{1,ik} \cdot \Delta Y_{ik}(t-1) + \varepsilon_{ik}(t)$$

mit $c_{ik}$ als Drift-Konstante, $\varphi_{1,ik}$ als Autokorrelationskoeffizient der Veränderungen und $\varepsilon_{ik}(t) \sim WN(0, \sigma^2)$ als White-Noise-Fehlerterm. Die Schätzung liefert zwei Größen, die jedes Unternehmen-Kennzahl-Paar in einem zweidimensionalen Merkmalsraum verorten:

**$\varphi_1$ (Mean-Reversion-Koeffizient):** Ein negatives $\varphi_1$ bedeutet, dass eine überdurchschnittliche Veränderung in Quartal $t-1$ im Folgequartal teilweise rückgängig gemacht wird. Bei $\varphi_1 = -0{,}43$ (Median für ROA) werden 43 % einer Quartalsveränderung im Folgequartal korrigiert. Ein $\varphi_1$ nahe null bedeutet, dass aufeinanderfolgende Veränderungen unkorreliert sind — das Modell hat keine Vorhersagekraft.

**$\sigma(\Delta Y)$ (Veränderungsvolatilität):** Die Standardabweichung der ersten Differenzen misst, wie stark eine Kennzahl typischerweise von Quartal zu Quartal schwankt. Diese Größe ist die Standardabweichung der gesamten transformierten Reihe $\Delta Y$, nicht die Residualvolatilität des AR-Modells.

Die Modellierung von Earnings-Persistenz als AR(1)-Prozess hat direkte Vorläufer in der Accounting-Literatur. Dichev und Tang (2009) schätzen AR(1)-Koeffizienten für Accruals und Cashflows und dokumentieren eine abnehmende Persistenz über die Zeit. Die vorliegende Arbeit erweitert diesen Ansatz in zwei Richtungen: Erstens werden sieben Kennzahlen aus drei Kategorien analysiert statt nur Earnings-Komponenten; zweitens werden erste Differenzen statt Niveaus modelliert, wodurch die Veränderungsdynamik statt der Niveaupersistenz im Fokus steht. Die FCF-Marge bildet dabei die direkteste Brücke zu Dichev und Tang, da sie die Cashflow-Komponente isoliert. Ihr $\varphi_1$-Median von $-0{,}46$ auf ersten Differenzen — verglichen mit den positiven Persistenzkoeffizienten auf Niveaus bei Dichev und Tang — illustriert den konzeptuellen Unterschied zwischen Veränderungskorrektur und Niveaupersistenz.

### Schritt 3: Individuelle Schätzung per OLS

Eine zentrale Designentscheidung ist die individuelle Schätzung per OLS für jede Unternehmen-Kennzahl-Kombination. Die Analyse umfasst 6.521 separate Regressionen (bis zu 932 Unternehmen × 7 Kennzahlen; für drei Unternehmen konnte je eine Kennzahl aufgrund unzureichender Datenqualität nicht geschätzt werden). Der Verzicht auf eine gepoolte Panel-Regression ist methodisch begründet: Pesaran und Smith (1995) zeigen, dass gepoolte Schätzer inkonsistent sind, wenn die Slope-Koeffizienten zwischen den Einheiten variieren. Da die vorliegende Arbeit gerade die Heterogenität der $\varphi_1$-Koeffizienten zwischen Unternehmen als Forschungsgegenstand hat, wäre eine Panel-Regression, die einen einheitlichen $\varphi_1$ unterstellt, inhaltlich kontraproduktiv.

Pesaran und Yang (2024) bestätigen diesen Befund spezifisch für heterogene AR(1)-Modelle in Kurzzeit-Panels: GMM-Schätzer unter der Annahme homogener Slopes sind verzerrt, wenn die wahren AR-Koeffizienten heterogen sind. Der von Pesaran und Smith (1995) vorgeschlagene Mean-Group-Estimator — individuelle OLS-Schätzung mit anschließender Mittelung der Koeffizienten — liefert konsistente Ergebnisse und entspricht exakt dem Design dieser Arbeit.

Mit $T = 98$ Beobachtungen pro Zeitreihe (100 Quartale abzüglich eines Lags für die Differenzenbildung und eines weiteren für den AR-Term) ist die Zeitdimension ausreichend für stabile OLS-Schätzungen. Signifikanz wird über $t$-Tests auf $\varphi_1 \neq 0$ geprüft ($p < 0{,}05$), und $R^2$ dient als Maß für die individuelle Modellgüte.

## 4.3 Quadrantenklassifikation

Die Schätzung des AR(1)-Modells liefert für jede der 6.521 Unternehmen-Kennzahl-Kombinationen zwei Größen: den Mean-Reversion-Koeffizienten $\varphi_1$ und die Veränderungsvolatilität $\sigma(\Delta Y)$. Diese beiden Dimensionen spannen einen zweidimensionalen Raum auf, in dem jedes Unternehmen-Kennzahl-Paar einen Punkt bildet. Die Quadrantenklassifikation teilt diesen Raum systematisch in vier Dynamiktypen.

### Konstruktion und Labels

Die Klassifikation erfolgt pro Kennzahl über einen Median-Split beider Dimensionen: Werte über dem kennzahlspezifischen Median werden als „hoch", Werte darunter als „niedrig" klassifiziert. Die Kombination ergibt vier Quadranten mit inhaltlichen Labels:

**Tabelle 4.2:** Quadrantenklassifikation — Labels und ökonomische Interpretation

| Quadrant | $\varphi_1$ | $\sigma(\Delta Y)$ | Ökonomische Interpretation |
|---|---|---|---|
| Korrektiv-Stabil | stark negativ | niedrig | Kleine Veränderungen, die sich systematisch umkehren — ruhige, selbstkorrigierende Dynamik |
| Korrektiv-Volatil | stark negativ | hoch | Große Ausschläge, die sich aber ebenfalls umkehren — turbulente Korrektur |
| Persistent-Stabil | nahe null | niedrig | Kaum Veränderung und keine Korrektur — träge, stabile Kennzahl |
| Persistent-Volatil | nahe null | hoch | Große Schwankungen ohne systematische Umkehr — unvorhersagbare Dynamik |

### Begründung des Median-Splits

Der Median-Split als Trennmechanismus ist eine methodische Entscheidung mit bekannten Vor- und Nachteilen. MacCallum, Zhang, Preacher und Rucker (2002) kritisieren die Dichotomisierung kontinuierlicher Variablen grundsätzlich und beziffern den Informationsverlust auf etwa 20 % der Parametergenauigkeit. Rucker, McShane und Preacher (2015) relativieren diese Kritik und zeigen, dass Median-Splits akzeptable Ergebnisse liefern, sofern die dichotomisierten Variablen nicht hoch korreliert sind — eine Bedingung, die in der vorliegenden Arbeit weitgehend erfüllt ist ($|\rho| < 0{,}19$ für Profitabilitätskennzahlen, $|\rho| \approx 0{,}19$–$0{,}24$ für Bilanzstruktur-Kennzahlen; vgl. Abschnitt 4.3.3).

Drei Argumente sprechen für den Median-Split gegenüber alternativen Klassifikationsmethoden wie K-Means: Erstens sind die resultierenden Labels direkt aus den Dimensionen abgeleitet und damit unmittelbar interpretierbar — „korrektiv" bedeutet starke Mean-Reversion, „volatil" bedeutet hohe $\sigma(\Delta Y)$. Zweitens ist die Zuordnung vollständig transparent und reproduzierbar. Drittens entspricht der Ansatz der etablierten Portfolio-Sort-Methodik in der empirischen Finanzforschung, wie sie etwa bei Fama und French (1993) für die Size- und Value-Sortierung verwendet wird. K-Means wird als datengetriebener Robustheitscheck in Kapitel 7 eingesetzt, um die Stabilität der Klassifikation zu prüfen.

### Validierung: Empirische Unabhängigkeit von $\varphi_1$ und $\sigma$

Eine potenzielle methodische Schwäche der Quadrantenklassifikation wäre eine mechanische Abhängigkeit der beiden Dimensionen: Höhere Volatilität könnte automatisch stärkere Mean-Reversion erzeugen, da größere Ausschläge häufiger zu Umkehrungen führen. In diesem Fall würde die Quadrantenklassifikation teilweise dieselbe Information doppelt verwenden.

Die empirische Prüfung dieser Frage erfolgt über Spearman-Rangkorrelationen zwischen $\varphi_1$ und $\sigma(\Delta Y)$ für jede der sieben Kennzahlen (vgl. Abbildung 4.2):

![Abb. 4.2: Spearman-Rangkorrelation ρ(φ₁, σ) pro Kennzahl. Alle Korrelationen liegen betragsmäßig unter 0,25. Bei Profitabilitätskennzahlen (blau) ist |ρ| < 0,19; nur Debt/Equity (rot) überschreitet diese Schwelle.](Kapitel_4_Grafiken/abb_4_4_phi1_sigma_korrelation.png)

**Tabelle 4.3:** Spearman-Rangkorrelation zwischen $\varphi_1$ und $\sigma(\Delta Y)$ pro Kennzahl. Niedrige Korrelationen belegen die empirische Trennbarkeit der beiden Dimensionen.

| Kennzahl | $N$ | Spearman $\rho$ | $p$-Wert | Einordnung |
|---|:---:|:---:|:---:|---|
| ROA | 931 | $-0{,}089$ | $< 0{,}01$ | sehr schwach |
| ROE | 931 | $-0{,}041$ | $0{,}213$ (n.s.) | nicht signifikant |
| EBIT-Marge | 932 | $-0{,}182$ | $< 0{,}001$ | schwach |
| FCF-Marge | 932 | $+0{,}045$ | $0{,}170$ (n.s.) | nicht signifikant |
| Current Ratio | 932 | $-0{,}187$ | $< 0{,}001$ | schwach |
| Debt/Equity | 931 | $-0{,}241$ | $< 0{,}001$ | schwach-moderat |
| Eigenkapitalquote | 932 | $-0{,}091$ | $< 0{,}01$ | sehr schwach |

Bei den vier Profitabilitätskennzahlen (ROA, ROE, EBIT-Marge, FCF-Marge) liegt $|\rho|$ durchgängig unter 0,19 — die beiden Dimensionen sind nur schwach korreliert. Die geringe Korrelation ist ökonomisch plausibel: Die Volatilität $\sigma(\Delta Y)$ wird primär durch Geschäftsmodell und Branche bestimmt — zyklische Nachfrage, operative Hebelwirkung, Saisonalität —, während die Korrekturgeschwindigkeit $\varphi_1$ eher von der Managementreaktion und Wettbewerbsdynamik abhängt, also davon, wie schnell ein Unternehmen auf Abweichungen vom Gleichgewicht reagiert. Diese Treiber sind konzeptuell verschieden, was die empirische Trennbarkeit erklärt.

Ergänzend bestätigt ein $\chi^2$-Test, dass die vier Quadranten für ROA, ROE, FCF-Marge und Eigenkapitalquote annähernd gleichverteilt sind (nicht signifikant). Die beiden Dimensionen sind empirisch trennbar, und die Quadrantenklassifikation nutzt tatsächlich zwei unabhängige Informationsdimensionen.

Für Debt/Equity und Current Ratio ist die Korrelation etwas stärker ($|\rho| \approx 0{,}19$–$0{,}24$), bleibt aber auf niedrigem Niveau. Diese Einschränkung wird bei der Interpretation der Bilanzstruktur-Kennzahlen in Kapitel 5 berücksichtigt.

Abbildung 4.3 illustriert die Quadrantenklassifikation am Beispiel ROA. Die gestrichelten Linien markieren die Median-Splits beider Dimensionen. Die Streuung der Unternehmen über alle vier Quadranten bestätigt visuell die niedrigen Korrelationswerte aus Tabelle 4.3 — Unternehmen mit starker Mean-Reversion finden sich sowohl bei niedriger als auch bei hoher Volatilität.

![Abb. 4.3: Quadrantenklassifikation am Beispiel ROA. Jeder Punkt repräsentiert ein Unternehmen im φ₁-σ-Raum. Die gestrichelten Linien markieren die Median-Splits beider Dimensionen. Die annähernde Gleichverteilung über alle vier Quadranten bestätigt die Trennbarkeit der Dimensionen.](Kapitel_4_Grafiken/abb_4_1_roa_quadrant.png)

## 4.4 Robustheitsdesign

Die Robustheit der Ergebnisse wird entlang dreier Dimensionen geprüft: Modellspezifikation, Stichprobenselektion und Quadrantenvalidierung. Dieser Abschnitt stellt das Design vor; die Ergebnisse werden in den jeweiligen Ergebniskapiteln berichtet.

### Modellwahl und Abgrenzung

Die Wahl von AR(1) auf ersten Differenzen als Hauptspezifikation wird durch drei implementierte Alternativen flankiert: AR(1) auf Niveaus, AR(2) auf ersten Differenzen und AR(1) auf saisonale Differenzen. Jede Alternative misst einen anderen Aspekt der Dynamik — Niveaupersistenz, längeres Gedächtnis bzw. saisonbereinigte Veränderungen. Die Wahl von AR(1) auf ersten Differenzen als Hauptmodell folgt dem Parsimonie-Prinzip und der inhaltlichen Passung zu FF1, die nach der Korrekturdynamik von Quartalsveränderungen fragt.

Darüber hinaus wurden zwei weitere Modellklassen erwogen, aber nicht implementiert. Ein VAR-Modell würde die simultane Dynamik mehrerer Kennzahlen innerhalb eines Unternehmens modellieren; die geringen querschnittlichen Korrelationen der $\varphi_1$-Koeffizienten zwischen Kennzahlenkategorien ($|\rho| < 0{,}10$; vgl. Kapitel 6) sprechen jedoch gegen relevante dynamische Interdependenzen auf der Ebene der AR-Parameter. GARCH-Modelle adressieren die bedingte Varianz, nicht den bedingten Mittelwert, und zeigen zudem erhebliche Konvergenzprobleme bei Quartalsdaten von Finanzkennzahlen (ARCH-LM-Voraussetzungen nur bei 23–42 % der Unternehmen erfüllt).

### Der Uniformitäts-Trade-off

Die Wahl einer einheitlichen Transformation (erste Differenzen) für alle sieben Kennzahlen stellt einen bewussten Trade-off zwischen statistischer Optimalität und querschnittlicher Vergleichbarkeit dar. Metrisch-spezifische Modellselektion — beispielsweise saisonale Differenzen für liquiditätsnahe Kennzahlen oder Niveau-basierte Schätzungen für träge Bilanzpositionen — würde die individuelle Modellanpassung verbessern, aber die zentrale Vergleichsanalyse zwischen Kennzahlenkategorien untergraben.

Die Forschungsfrage FF1 fragt nach „systematischen Dynamik-Unterschieden zwischen Finanzkennzahlen". Diese Frage erfordert, dass die Dynamik-Maße ($\varphi_1$, $\sigma$) über Kennzahlen hinweg vergleichbar sind. Würde ROA auf ersten Differenzen und Eigenkapitalquote auf Niveaus modelliert, würden die resultierenden $\varphi_1$-Werte konzeptuell Verschiedenes messen — der querschnittliche Vergleich wäre ungültig. Die $\varphi_1$-Werte dieser Arbeit messen daher nicht „die wahre Persistenz" einer Kennzahl, sondern die Autokorrelationsstruktur der Quartalsveränderungen unter einheitlicher Differenzierungsannahme. Die Begründung für diese Wahl folgt der Argumentationslinie von Fairfield und Yohn (2001) sowie Dichev und Tang (2009), die Veränderungen als informativere Größe für die Dynamikanalyse identifiziert haben.

### Alternative AR-Spezifikationen

Neben dem Hauptmodell (AR(1) auf ersten Differenzen, nachfolgend „diff1") werden drei alternative Spezifikationen geschätzt, die jeweils eine andere Perspektive auf die Dynamik bieten:

**Tabelle 4.4:** Übersicht der vier AR-Spezifikationen

| Variante | Modellgleichung | Was wird getestet? |
|---|---|---|
| diff1 (Haupt) | $\Delta Y(t) = c + \varphi_1 \cdot \Delta Y(t-1) + \varepsilon(t)$ | Korrekturgeschwindigkeit der Quartalsveränderungen |
| levels | $Y(t) = c + \varphi_1 \cdot Y(t-1) + \varepsilon(t)$ | Niveaupersistenz (komplementäre Perspektive) |
| ar2_diff1 | $\Delta Y(t) = c + \varphi_1 \cdot \Delta Y(t-1) + \varphi_2 \cdot \Delta Y(t-2) + \varepsilon(t)$ | Zusätzliche Lag-2-Struktur |
| diff4 | $\Delta_4 Y(t) = c + \varphi_1 \cdot \Delta_4 Y(t-1) + \varepsilon(t)$ | Saisonbereinigte Dynamik ($\Delta_4 Y = Y(t) - Y(t-4)$) |

Die Levels-Variante beantwortet die komplementäre Frage nach der Niveaupersistenz. Eine Kennzahl mit hohem $\varphi_1$ auf Niveaus und niedrigem $|\varphi_1|$ auf Differenzen — wie die Eigenkapitalquote ($\varphi_{1,\text{levels}} = 0{,}93$; $\varphi_{1,\text{diff1}} = -0{,}04$) — hat ein sehr stabiles Niveau, dessen Quartalsveränderungen nahezu unkorreliert sind. Das AR(2)-Modell testet, ob ein einzelner Lag die Autokorrelationsstruktur ausreichend erfasst. Die saisonale Differenz $\Delta_4 Y$ eliminiert mögliche Saisonmuster und prüft, ob die negativen $\varphi_1$-Werte auf ersten Differenzen teilweise saisonale Artefakte sind. Da $\Delta_4 Y$ vier Quartale statt eines verbraucht, reduziert sich die effektive Zeitreihenlänge auf $T = 95$ Beobachtungen (nach Differenzierung und einem AR-Lag), was die Schätzpräzision gegenüber dem Hauptmodell leicht verringert.

**Tabelle 4.5:** $\varphi_1$-Mediane unter vier AR-Spezifikationen. Die Drei-Schichten-Hierarchie bleibt modellübergreifend stabil.

| Kennzahl | diff1 | levels | ar2 ($\varphi_1$) | diff4 |
|---|:---:|:---:|:---:|:---:|
| ROA | $-0{,}43$ | $+0{,}36$ | $-0{,}56$ | $+0{,}21$ |
| ROE | $-0{,}43$ | $+0{,}32$ | $-0{,}55$ | $+0{,}21$ |
| EBIT-Marge | $-0{,}43$ | $+0{,}36$ | $-0{,}55$ | $+0{,}21$ |
| FCF-Marge | $-0{,}46$ | $+0{,}10$ | $-0{,}60$ | $+0{,}12$ |
| Current Ratio | $-0{,}17$ | $+0{,}80$ | $-0{,}21$ | $+0{,}59$ |
| Debt/Equity | $-0{,}09$ | $+0{,}87$ | $-0{,}10$ | $+0{,}66$ |
| Eigenkapitalquote | $-0{,}04$ | $+0{,}93$ | $-0{,}04$ | $+0{,}72$ |

Abbildung 4.4 visualisiert die Ergebnisse über alle vier Spezifikationen hinweg.

![Abb. 4.4: φ₁-Mediane unter vier AR-Spezifikationen. Die Drei-Schichten-Hierarchie (Profitabilität → Liquidität → Kapitalstruktur) bleibt modellübergreifend stabil, unabhängig davon, ob auf Differenzen, Niveaus, mit zwei Lags oder saisonal differenziert geschätzt wird.](Kapitel_4_Grafiken/abb_4_3_modellvergleich.png)

Die Ergebnisse bestätigen ein konsistentes Muster: Bei den Profitabilitätskennzahlen korrespondiert die starke Quartalskorrektur (diff1: $-0{,}43$ bis $-0{,}46$) mit moderater Niveaupersistenz (levels: $0{,}10$–$0{,}36$) und geringer Persistenz der Jahresveränderungen (diff4: $0{,}12$–$0{,}21$). Bei den Kapitalstruktur-Kennzahlen ist das Bild invers: Kaum Quartalskorrektur (diff1: nahe null) bei extrem hoher Niveaupersistenz (levels: $0{,}87$–$0{,}93$) und persistenten Jahresveränderungen (diff4: $0{,}66$–$0{,}72$). Die Current Ratio liegt in allen Spezifikationen zwischen diesen beiden Gruppen. Die Drei-Schichten-Hierarchie ist somit kein Artefakt der Transformationswahl, sondern manifestiert sich unabhängig von der gewählten Modellspezifikation. Die Robustheitshypothese — Rangordnungsstabilität über alle vier Varianten — ist bestätigt (die detaillierten Ergebnisse werden in Kapitel 5 diskutiert).

### Variable Stichproben

Die Abhängigkeit der Ergebnisse vom Vollständigkeitsfilter wird durch vier Stichproben mit unterschiedlichen Mindest-Quartalsanforderungen getestet. Alle Stichproben durchlaufen identische Aufbereitungsschritte (Outlier-Detection, NaN-Filter, Winsorisierung); der einzige Unterschied ist die geforderte Mindestanzahl an Quartalen.

**Tabelle 4.6:** Stichprobengrößen bei variablen Vollständigkeitsschwellen

| Stichprobe | Min. Quartale | Unternehmen | AR-Schätzungen |
|---|:---:|:---:|:---:|
| 100Q (Hauptanalyse) | 100 | 932 | 6.521 |
| 80Q | 80 | 1.231 | 8.613 |
| 60Q | 60 | 1.855 | 12.977 |
| 40Q | 40 | 2.356 | 16.484 |

Der Vergleich über Stichproben adressiert direkt den Survivorship Bias: Die erweiterten Stichproben enthalten Unternehmen, die erst nach 2000 gelistet oder vor 2024 delistet wurden. Wenn die $\varphi_1$-Mediane dennoch stabil bleiben, ist der Bias für die Kernbefunde irrelevant (vgl. Abbildung 4.5). Die detaillierten Ergebnisse werden in Abschnitt 5.5 berichtet.

![Abb. 4.5: φ₁-Mediane über variable Stichproben. Die Profitabilitätskennzahlen (links) zeigen nahezu identische Werte unabhängig von der Stichprobengröße (Abweichung < 3 %). Bei Kapitalstruktur-Kennzahlen (rechts) sind die Abweichungen größer, ohne die qualitative Einordnung zu verändern.](Kapitel_4_Grafiken/abb_4_5_stichproben_stabilitaet.png)

### Weitere Robustheitschecks

Zwei weitere Robustheitsdimensionen ergänzen das Design: Erstens wird in Kapitel 7 eine separate Analyse des Finanzsektors durchgeführt, um die Auswirkungen der Sektorexklusion zu quantifizieren. Zweitens wird eine K-Means-Clusteranalyse ($k = 2$) auf den AR-Parametern als datengetriebener Vergleich zur theoriegeleiteten Quadrantenklassifikation eingesetzt (ebenfalls Kapitel 7).

## 4.5 Statistische Testverfahren

Die drei Forschungsfragen erfordern unterschiedliche statistische Testverfahren, die in diesem Abschnitt überblicksartig vorgestellt werden. Detailliertere Erläuterungen erfolgen jeweils in den Ergebniskapiteln.

### FF1: Deskription und Verteilungsvergleiche

Für FF1 stehen deskriptive Statistiken (Median, Interquartilsabstand, Signifikanzraten, $R^2$-Verteilungen) im Vordergrund. Die zentrale These — die Drei-Schichten-Hierarchie — wird primär visuell und durch Vergleich der Mediane etabliert. Ergänzend werden Mann-Whitney-U-Tests eingesetzt, um paarweise Unterschiede in den $\varphi_1$-Verteilungen zwischen Kennzahlenpaaren auf statistische Signifikanz zu prüfen. Der Mann-Whitney-Test ist als nichtparametrischer Test robust gegenüber Verletzungen der Normalverteilungsannahme, die bei AR-Koeffizienten typisch ist.

### FF2: Interdependenzmaße und Event-Analyse

Die Interdependenzanalyse (FF2) verwendet zwei Instrumente. Spearman-Rangkorrelationen messen den monotonen Zusammenhang zwischen den $\varphi_1$-Werten (bzw. $\sigma$-Werten) verschiedener Kennzahlen über alle 932 Unternehmen. Die Wahl von Spearman statt Pearson ist durch die schiefe Verteilung der AR-Parameter begründet; die Rangkorrelation ist zudem robust gegenüber Ausreißern in den Endverteilungen.

Für die datengetriebene Event-Analyse werden Hochvolatilitätsphasen identifiziert: Quartale, in denen mindestens drei der sieben Kennzahlen gleichzeitig das 90. Perzentil der Querschnittsvolatilität überschreiten. Die Querschnittsvolatilität ist dabei als Standardabweichung der $|\Delta Y|$-Werte über alle 932 Unternehmen in einem gegebenen Quartal definiert. In diesen Phasen werden die Verteilungen der ersten Differenzen nach Quadrantentyp verglichen, wobei Mann-Whitney-U-Tests und Kruskal-Wallis-Tests eingesetzt werden. Bei multiplem Testen über sieben Kennzahlen und drei Event-Fenster wird das Bonferroni-korrigierte Signifikanzniveau $\alpha^* = 0{,}05/k$ angegeben, wobei $k$ die Anzahl simultaner Tests innerhalb einer Testfamilie ist. Ergänzend werden die unkorrigierten $p$-Werte berichtet und als solche gekennzeichnet, da die Bonferroni-Korrektur bei korrelierten Teststatistiken konservativ ist (vgl. Abschnitt 6.4).

### FF3: Assoziationsmaße und externe Validierung

Die externe Validierung (FF3) prüft, ob die Quadrantenzuordnung durch beobachtbare Strukturmerkmale erklärbar ist. $\chi^2$-Unabhängigkeitstests testen die Assoziation zwischen Branchenzugehörigkeit und Quadrantentyp für jede der sieben Kennzahlen separat; das Bonferroni-korrigierte Signifikanzniveau liegt bei $\alpha^* = 0{,}05/7 \approx 0{,}007$. Cramérs $V$ dient als Effektstärkemaß zur Quantifizierung der Assoziationsstärke — die Anwendung auf kategorial-kategoriale Daten (Sektor × Quadrant) ist methodisch korrekt, da keine Diskretisierung metrischer Variablen erforderlich ist.

Spearman-Rangkorrelationen messen den Zusammenhang zwischen Unternehmensgröße (Mitarbeiterzahl, Marktkapitalisierung) und den AR-Parametern ($\varphi_1$, $\sigma$). Eine K-Means-Clusteranalyse auf den AR-Parametern aller sieben Kennzahlen (14-dimensionaler Merkmalsraum: je ein $\varphi_1$ und ein $\sigma$ pro Kennzahl) dient als datengetriebener Vergleich zur Quadrantenklassifikation.

Konsistenz-Scores erfassen, in welchem Anteil der sieben Kennzahlen ein Unternehmen demselben Quadranten zugeordnet wird. Dieser Score adressiert die Frage, ob die Quadrantenklassifikation primär kennzahlspezifisch oder unternehmensspezifisch ist — eine zentrale Frage für die praktische Anwendbarkeit der Klassifikation.

### Konfirmatorisch vs. explorativ

Die statistische Analyse unterscheidet zwischen konfirmatorischen und explorativen Elementen. Die Drei-Schichten-Hierarchie (FF1) und die Sektorabhängigkeit der Quadranten (FF3) werden als Hypothesen getestet und unterliegen den oben genannten Signifikanzkorrekturverfahren. Die Event-Analyse (FF2) und die K-Means-Clusteranalyse haben explorativen Charakter und dienen der Musteridentifikation, nicht der Hypothesenprüfung. Diese Unterscheidung wird in den jeweiligen Ergebniskapiteln bei der Signifikanzinterpretation explizit benannt.

---

*Das folgende Kapitel (Kapitel 5) präsentiert die Ergebnisse zu FF1 und wendet die hier beschriebenen Methoden auf die Identifikation und Charakterisierung der Drei-Schichten-Hierarchie an.*
