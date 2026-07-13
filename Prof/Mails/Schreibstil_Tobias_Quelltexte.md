Sehr geehrter Herr Prof. Steglich, sehr geehrter Herr Prof. Stollhoff,


in Woche 7 meines Arbeitsprozesses an meiner Masterarbeit möchte ich Ihnen hier einen Zwischenstand zu meinen bisherigen Ergebnissen geben.

Mit der Datenaufbereitung bin ich fertig in dieser Form:
Datenbasis: 5871 Unternehmen
Exklusion von ADRs zur reinen US Betrachtung
Unternehmen mit lückenlosem Datensatz über alle 100 Quartale: 976 Unternehmen (wird zur Untersuchung einzelner Zeiträume aber jeweils angepasst)
Rolling-Window Outlier Detection auf Rohwerte (unten eine kurze Erklärung dazu)
NaN / 0 - Qualitätsfilter: Unternehmen mit 10% fehlenden Werten werden ausgeschlossen (44 Unternehmen weniger)
Berechnung von 7 Kennzahlen: ROA, ROE, EBIT-Marge, FCF-Marge, Current Ratio, Debt-to-Equity, Eigenkapitalquote (Erweiterung kann ohne Probleme umgesetzt werden)
Winsorisierung der Kennzahlen: Begrenzt Extremwerte durch ~ 0 Nenner
Ergebnis: 932 Unternehmen × 100 Quartale.


Genaueres zur Outlier-Methodik:

Auf Rohwert-Ebene verwende ich ein Multi-Window Rolling-Z-Score-Verfahren (Fenster = 8 Quartale, σ = 3). Ein Wert wird nur markiert, wenn
mindestens 3 Fenster ihn markiert haben
Die Abweichung >5 beträgt

So ergeben sich nur noch 600 Werte, welche überprüft werden müssen, um API Fehler zu minimieren


Zu FF1 kann ich bereits einige Ergebnisse sagen:
Die AR(1)-Schätzung auf ersten Differenzen ergibt eine Hierarchie:
Profitabilitätskennzahlen zeigen starke Mean-Reversion (φ₁ ≈ −0.43 bis −0.46)
Liquidität moderate (φ₁ ≈ −0.17)
Kapitalstruktur kaum (φ₁ ≈ −0.04 bis −0.09)

Diese Hierarchie (und auch die Messung der Volatilität) ist soweit auch mit den untersuchten Branchen stimmig, welche erklärbare Dynamiken zeigen.


Für FF2 und FF3 arbeite ich aktuell an der Auswertung.
Bei FF2 untersuche ich die Zusammenhänge der Dynamik-Profile zwischen den Kennzahlen über Korrelationsanalysen und Kreuztabellen und habe die Analyse um eine Event-basierte Komponente erweitert, die zeigt, wie sich die Dynamik-Typen in Stressphasen verhalten.
Bei FF3 validiere ich die Quadrantenklassifikation gegen externe Strukturmerkmale (Branche, Größe) und nutze K-Means als zusätzlichen Robustheitscheck.


Offene methodische Punkte:

GAAP vs. IFRS:
	Die EODHD-Daten stammen aus SEC-Filings (US-GAAP). Eine Garantie für reine US-GAAP-Daten ist bei EODHD jedoch nicht möglich (meine Filterungen helfen dabei schon),
	aber ich werde dies als Limitation in meiner Arbeit nennen. Eine reine Betrachtung nach IFRS würde eine andere API und Ausschluss vieler Unternehmen bedeuten, da native US-Firmen selten in IFRS 
	berichten. Für den (noch geplanten) Export der EU-Unternehmen werde ich überwiegend IFRS Daten bekommen.
	Wissen Sie, ob ich damit arbeiten kann, oder sollte ich USA und EU ausschließlich einzeln betrachten und keinen realen Vergleich zwischen Regionen einbeziehen?

Survivorship Bias:
	Der Filter auf 100 Quartale schränkt die Stichprobe auf langlebige Unternehmen ein (932 von 5871). Die Ergebnisse für FF1 und FF3 gelten damit primär für etablierte Unternehmen, 
	nicht für den Gesamtmarkt. Z.Bsp. Erkennbar anhand der Technologie Unternehmen, welcher während der Dot-Com-Krise in meinen Daten erstaunlich wenig Auffällig sind.
	In der FF2 wird jedoch der Datensatz erweitert, sodass ich auch Unternehmen betrachten möchte, welche 2025 nicht mehr existieren (keine Filterung auf 100 Quartale).

Saisonalität und andere AR-Modelle:
	Aktuell verwende ich einfache erste Differenzen (Q2-Q1). Saisonale Differenzen (Q1-Vorjahres Q1) wären eine Alternative, die ich momentan evaluiere.
	Da dies jedoch einfach eine weitere Version des AR Modells wäre (AR(4)), habe ich mich gefragt, ob man nicht Pro Kennzahl generell einen Vergleich zwischen den AR Modellen anwenden könnte.
	Würden sie meinen, dass neben der Saisonalen Betrachtung, die Interpretation von z.Bsp. ROA mit AR(1) im Vergleich zu D/E mit AR(2) möglich und sinnvoll wäre?

Ich hoffe ich konnte Ihnen einen sinnvollen Überblick über meinen aktuellen Forschungsstand verschaffen und würde mich sehr freuen eine kurze Einschätzung von Ihnen bezüglich der unterschiedlichen AR-Modelle und dem GAAP vs. IFRS zu erhalten. 
Wie bereits beim letzten Treffen besprochen würde ich mich freuen, wenn wir in 2-3 Wochen den nächsten gemeinsamen Termin ansetzen könnten. Hätten Sie vielleicht schon einen Terminvorschlag, der Ihnen passen würde?


Mit freundlichen Grüßen

Tobias Mourier



Als Anhang mein zeitlicher Ablauf:

Bisher:
W1/2:	Datenakquise, Pipeline-Entwurf, Kennzahlenauswahl
W3:		Operationalisierungsdokument, Treffen mit Prof zur methodische Festlegungen
W4/5:	AR(1)-Schätzung, Quadrantenklassifikation, Datenaufbereitung (fertige Filterkette, NaN-Bereinigung)
W6/7:	Datenqualität (Outlier Detection, Winsorisierung), Robustheitsanalysen, Modellvergleich, Ergebnisse zu FF1
W8:		Erste Konzeption FF2/FF3 zur Vorbereitung methodischer Fragen

Geplant:
W9: 		Zweites Treffen, methodische Abstimmung zu FF2/FF3
W10/11: 	Umsetzung FF2: Korrelationsanalysen, Kreuztabellen, Event-basierte Analyse
W12/13: 	Umsetzung FF3: x²-Tests, Größeneffekte, Robustheitschecks
W14: 	Verschriftlichung: Einleitung, Theorie, Methodik
W15-17:	Verschriftlichung: Ergebnisse, Diskussion
W18: 	Revision, Formatierung
Abgabe:	21. Mai


---

Sehr geehrter Herr Prof. Stollhoff, sehr geehrter Herr Prof. Steglich,

Vielen Dank für Ihre Rückmeldung und die hilfreiche Einordnung der AR-Modellvarianten.
Als Vorbereitung auf unser Gespräch möchte ich Ihnen gerne einen konkreteren Einblick in meine Durchführung und Ergebnisse geben, insbesondere der Beantwortung von FF1 sowie der Ausgestaltung von FF2 und FF3.

Zum Termin:
Donnerstag, 26.3. passt gut. Ich bin ab 9 Uhr flexibel und richte mich nach Ihnen.
Prof. Steglich, passt der Termin auch für Sie? Die Frage zur GAAP / IFRS Abgrenzung würde ich gerne bei dieser Gelegenheit mit Ihnen besprechen, dafür kann ich auch gerne noch weitere Informationen mitbringen.


Die Datenbasis und Aufbereitung ist gegenüber meiner letzten Mail unverändert.

FF1: Weisen Finanzkennzahlen über Unternehmen hinweg systematische Unterschiede in ihrer zeitlichen Dynamik auf?

Die Modellwahl, 3-Schichten-Hierarchie & Quadranten-Framework habe ich in einem separaten Dokument im Anhang aufbereitet.

FF2: Welche Interdependenzen bestehen zwischen Finanzkennzahlen, und inwieweit unterscheiden sich diese zwischen Unternehmen? 

Im Querschnitt (alle Unternehmen) prüfe ich über Spearman-Korrelationen der phi- und sigma-Werte (Mean Revision & Volatilität) sowie Cramer's V auf den Quadrantenzuordnungen, ob z.Bsp. ein Unternehmen mit starker Mean-Reversion bei ROA dieses Muster auch bei der EBIT-Marge, usw. zeigt.
Die bisherigen Ergebnisse bestätigen die Blockstruktur aus FF1: Innerhalb der Kategorien sind die Profile stark korreliert, cross-kategorial aber deutlich schwerer zu vergleichen.
Das liegt auch daran, dass die Kennzahlen innerhalb der Kategorien mathematische zusammenhänge haben, da wäre es bestimmt auch interessant andere Kennzahlen zu prüfen, um die These ausführlicher zu testen.

Die Grafik zeigt die rollierende Querschnittsvolatilität über den gesamten Beobachtungszeitraum. Die markierten Zeitfenster wurden datengetrieben identifiziert und passen jeweils zu Krisenzeitpunkten.
Die unterschiedlichen Skalen der Kennzahlen erschweren den Vergleich zwischen den Kategorien auf einer Achse. Die Grafik dient daher primär der zeitlichen Einordnung der Krisenreaktionen.
Im nächsten Schritt vergleiche ich, ob korrektive & persistente Unternehmen in den Zeitfenstern unterschiedlich reagieren.


FF3: Stehen zeitliche Dynamiken von Finanzkennzahlen in Zusammenhang mit strukturellen Unternehmensmerkmalen?

FF3 prüft, ob die Quadrantenklassifikation und andere Erkenntnisse aus FF1 durch externe Strukturmerkmale erklärbar sind.
Für Brancheneffekte nutze ich x² Tests und Cramer's V, für Größeneffekte Spearman-Korrelationen von MarketCap und Mitarbeiterzahl mit phi und sigma. Als Gegencheck setze ich später auch noch K-Means auf den AR-Parametern ein.

Die Grafik zeigt den Größeneffekt über die Mitarbeiterzahl: Größere Unternehmen zeigen konsistent niedrigere Volatilität, am stärksten bei FCF-Marge und Current Ratio, deutlich auch bei EBIT-Marge.
Die Mean-Reversion wird dagegen kaum beeinflusst (p Werte nahe 0).
Größe wirkt als Volatilitäts-„Puffer", beeinflusst aber nicht den Korrekturmechanismus.


Die Grafiken und Ergebnisse werde ich bis zum Termin noch besser und ausführlicher darstellen können.

Vielen Dank für Ihre Zeit und Mühe.

Mit freundlichen Grüßen
Tobias Mourier


---

Sehr geehrter Herr Prof. Stollhoff, sehr geehrter Herr Prof. Steglich,

vielen Dank für die so schnelle Rückmeldung.

Zum Termin:
Ich würde beim Donnerstag um 9 Uhr bleiben.
Prof. Steglich, falls Ihnen ein anderer Zeitpunkt besser passt, richte ich mich gerne nach Ihnen, ansonsten bleibt es bei 9 Uhr.

Prof. Stollhoff, die Nachfrage nach den Modellgleichungen möchte ich vorab klären.

Die vier Spalten der Tabelle entsprechen vier AR Spezifikationen:
diff1 (ΔY): AR(1) auf erste Differenzen:
ΔY(t) = c + φ · ΔY(t−1) + ε(t)
φ misst die Autokorrelation der Quartalsveränderungen. Ein negatives φ bedeutet: Überdurchschnittliche Veränderungen werden im Folgequartal teilweise korrigiert.
Levels (Y): AR(1) auf Niveaus:
Y(t) = c + φ · Y(t−1) + ε(t)
φ misst die Niveaupersistenz. Ein Wert nahe 1 bedeutet, das Niveau ändert sich von Quartal zu Quartal kaum (hohe Persistenz).
AR(2) φ1: AR(2) auf erste Differenzen:
ΔY(t) = c + φ1 · ΔY(t−1) + φ2 · ΔY(t−2) + ε(t)
φ1 und φ2 sind Autoregressionskoeffizienten bei Lag 1 & 2. Der zweite Lag prüft, ob ein längeres „Gedächtnis“ der Veränderungen vorliegt und verändert somit den Wert vom φ1.
diff4 (Δ₄Y): AR(1) auf Jahresveränderungen (Δ₄Y(t) = Y(t) − Y(t−4)):
Δ₄Y(t) = c + φ₁ · Δ₄Y(t−1) + ε(t)
φ₁ misst die Autokorrelation der Jahresveränderung. Bei hohen Werten setzten sich Jahrestrends fort.

￼

Bei Profitabilität korrespondiert die starke Quartalskorrektur (diff1: −0,43 bis −0,46) mit niedriger Niveaupersistenz (levels: 0,10 – 0,57) und geringer Persistenz der Jahresveränderungen (diff4: 0,12 – 0,30).
Bei Kapitalstruktur ist es umgekehrt: Kaum Quartalskorrektur (diff1: nahe null) bei extrem hoher Niveaupersistenz (levels: 0,87 & 0,93) und persistenten Jahresveränderungen (diff4: 0,66 & 0,72).
Die Current Ratio liegt in allen Spezifikationen dazwischen.

Ich hoffe ich konnte den Umstand zufriedenstellend darstellen.
Bis auf die Interpretation sollte ich Ihre Fragen beantwortet haben, denke ich.

Mit freundlichen Grüßen
Tobias Mourier


---

FF1: Systematische Dynamik-Unterschiede von Finanzkennzahlen 
1. Methodik 
Das AR(1)-Modell wird auf die erste Differenz jeder Kennzahl angewendet: 
ΔY(t) = c + φ₁ · ΔY(t−1) + ε(t) 
 
Daraus ergeben sich zwei zentrale Parameter: 
• 
Mean-Reversion-Stärke (φ): 
Misst die Autokorrelation der Veränderungen. Ein negativer φ bedeutet: Überdurchschnittliche 
Quartalsveränderungen werden im Folgequartal teilweise korrigiert. (Bei -0,40 wird eine 
Veränderung zu 40% zurückgenommen) 
 
            
 
Anschauungsbeispiel: starke & schwache Mean-Reversion (Kennzahl / φ) 
 
• 
Änderungsvolatilität (σ(ΔY)): 
Misst die typische Quartal / Quartal - Schwankung. Ein Maß für die Unruhe im Zeitverlauf. 
 
Zusammen spannen φ₁ und σ(ΔY) einen Raum auf, in dem vier Dynamik-Typen über einen Median-Split 
unterschieden werden (Quadrantenklassifikation bei ROA): 
 
 
  
 
 


 
 
2. Modellvergleich / Robustheit 
Die Wahl von AR(1) auf ersten Differenzen als Primärmodell wurde durch drei AR-Spezifikationen validiert. 
Die erkannte Hierarchie bleibt in allen Varianten erhalten: 
Auf Levels zeigt Kapitalstruktur die höchste Persistenz (0,87–0,93), Profitabilität nur moderat (0,10–0,36). 
Ein zweiter AR-Lag bringt bei Profitabilität zusätzliche Erklärungskraft (R² steigt 0,19 -> 0,29), verändert 
aber die qualitative Aussage nicht. 
 
 
 
Die folgenden Kernbefunde sind damit modellunabhängig. 
3. Ergebnisse (Kennzahl-Hierarchie): 
Die im folgenden beschriebene Hierarchie ist grundsätzlich ökonomisch erklärbar durch die 
Unterscheidung von 
• 
Markt-   
 
 
(Proﬁtabilität: Konjunktur, Wettbewerb) 
• 
& Managementgesteuerter  
(Bilanzstruktur: Finanzierungsentscheidungen) 
Kennzahlen und spiegeln auch die Herkunft der Kennzahlen wieder. 
 
Die Boxplots zeigen die drei Schichten der Hierarchie über alle 932 Unternehmen: 
 
 
• 
Proﬁtabilität (-0,43 bis -0,46): 
zeigt konsistente, starke Mean-Reversion. 
90 - 97% der Unternehmen haben signiﬁkante Eoekte, R² liegt bei 0,18 - 0,21. 
Die vier Kennzahlen clustern eng. Trotz unterschiedlicher Berechnungsgrundlage (Buchgewinn / 
Cashﬂow) sind Quartalsveränderungen in operativen Performances temporär. 


• 
Liquidität (-0,17): 
Die Current Ratio liegt in der Mitte der Hierarchie. 
Nur 46% der Unternehmen zeigen signiﬁkante Mean-Reversion, R² = 0,03. 
Liquiditätsentscheidungen sind teilweise systematisch, teilweise diskretionär. 
• 
Kapitalstruktur (-0,04 bis -0,09): 
Debt-to-Equity und Eigenkapitalquote zeigen kein AR-Signal auf Dioerenzen. 
Veränderungen der Kapitalstruktur sind Managemententscheidungen, die keinem AR Prozess folgen. 
Auf Niveaus dagegen höchste Persistenz (0,87 - 0,93). 
 
 
 
4. Sektorale Analyse 
Innerhalb der Drei-Schichten-Hierarchie variieren die Parameter sektoral. Die Heatmap zeigt die φ₁-
Mediane pro Sektor und Kennzahl. 
 
• 
Communication Services 
zeigt die stärkste Mean-Reversion bei Proﬁtabilität (−0,49). 
Hohe Fixkosten, Umsatzschwankungen zeigen sich direkt. 
• 
Basic Materials 
haben die schwächste Mean-Reversion bei Proﬁtabilität (ca. −0,40). 
Rohstoopreise treiben die Proﬁtabilität 
• 
Real Estate 
sticht bei der Current Ratio hervor (−0,34). 
Durch Reﬁnanzierungen entsteht eine hohe Liquiditätsdynamik. 


• 
Utilities 
zeigen als einziger Sektor Mean-Reversion bei Kapitalstruktur-Kennzahlen (−0,17 & −0,14). 
Die regulierte Kapitalstruktur erzeugt ein systematisches Zurückkehren zum Zielwert. 
 
 
Die Quadranten dioerenziert die Sektoren weiter (siehe hierzu auch Scatter-Chart – S. 1): 
 
• 
Bei Communication Services und Energy dominiert der korrektiv-volatile Typ. 
Große Ausschläge, die systematisch korrigiert werden.  
• 
Basic Materials und Technology fallen durch den höchsten Anteil persistent-volatiler 
Unternehmen auf. 
Hier ist die Proﬁtabilitätsdynamik am wenigsten vorhersagbar. 
• 
In den übrigen Sektoren überwiegen stabile Proﬁle.


---

