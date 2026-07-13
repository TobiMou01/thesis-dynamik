# Drehbuch Kolloquium — 07.07.2026 · 20 Minuten · 14 logische Seiten

**Eckdaten:** Vortrag 20 Min. + Diskussion · Prüfer: Prof. Steglich (Kennzahlen/BWL-Seite) und Prof. Stollhoff (Zeitreihen-Seite — von ihm kommt mit hoher Wahrscheinlichkeit die Differenzen-Benchmark-Frage; Seite 9 ist seine Folie). Durchgängig Morph, Build-Folien teilen sich eine logische Seitenzahl (wie deine „02/13"-Logik). Neue Zählung: **/14**.

**Vier Prinzipien für alle weiteren Folien:**
1. **Folie = Behauptung + Beleg.** Titel als Aussagesatz (machst du bei „Struktur erklärt σ — nicht φ" schon), darunter genau eine Grafik oder eine Zahlengruppe. Alles Argumentative wandert in den Redetext.
2. **Der φ-σ-Raum ist der rote Faden.** Er wird auf Seite 6 leer aufgebaut, füllt sich auf Seite 7 per Morph mit den Schichten, und seine Punkte fallen auf Seite 9 auf die Benchmark-Achse. Methodik wird so zum Anlauf auf die Ergebnisse.
3. **Der Rahmen schließt sich.** Die drei FF-Karten von Seite 3 kehren auf Seite 14 per Morph zurück und bekommen ihre Antworten angeheftet. Null Bauaufwand, maximale Wirkung.
4. **Farbcode konsequent** (aus deinem Deck ausgelesen): Hintergrund `1E402E`, Karten `4A6D56`, Text `F2EFDA`, Sage `B3BC9A`, Akzent Blau `78A2F9`, Akzent Gelb `E6D44F`. Kennzahlgruppen durchgängig: **Profitabilität = Blau `78A2F9` · Liquidität = Gelb `E6D44F` · Kapitalstruktur = Koralle `E8867C`** (falls noch kein Rotton definiert ist). Jede neue Grafik nutzt exakt diese Zuordnung.

---

## Ablaufübersicht (Soll: 19:30–20:00)

| Seite | Inhalt | Zeit | Status |
|---|---|---|---|
| 1 | Titel | 0:30 | fertig |
| 2 | Einleitung: Dynamik, φ & σ | 1:15 | fertig |
| 3 | Forschungsfragen + Beitrag | 1:15 | fertig |
| 4 | Daten: Filterkette | 1:00 | fertig — Redetext straffen |
| 5 | Methodik: AR(1) + **NEU G1 Intuitionsgrafik** | 1:45 | in Arbeit |
| 6 | Methodik: Quadranten (φ-σ-Bühne) | 1:15 | in Arbeit |
| 7 | FF1: Drei Dynamiktypen (**G4 Dark-Render**) | 2:00 | neu bauen |
| 8 | FF1: Warum? Strom/Bestand + Markt/Management | 1:45 | Platzhalter überarbeiten |
| 9 | **NEU: Benchmark-Einordnung (G2)** | 1:15 | neu bauen |
| 10 | FF2: Matrizen-Kontrast | 1:30 | Platzhalter überarbeiten |
| 11 | FF2: Krisenphasen | 1:15 | Platzhalter überarbeiten |
| 12 | FF3: Asymmetrie + **NEU G3 Restinformation** | 2:00 | neu bauen |
| 13 | Limitationen | 1:15 | Platzhalter (Tippfehler „AUSBLCK") |
| 14 | Fazit: FF-Karten kehren zurück + Ausblick | 2:00 | neu bauen |

Gewichtung: Seiten 1–6 ≈ 7:00 (35 %), Seiten 7–14 ≈ 13:00 (65 %) — genau die Verschiebung, die du wolltest. Validierung fliegt als eigene Seite raus und wird Backup B1.

---

## Folien-für-Folien-Drehbuch

### Seite 1 — Titel (0:30) · fertig

**Redetext:**
„Sehr geehrter Herr Professor Steglich, sehr geehrter Herr Professor Stollhoff, vielen Dank für die Gelegenheit, meine Masterarbeit vorzustellen. Ich habe untersucht, wie sich Finanzkennzahlen börsennotierter US-Unternehmen über die Zeit verhalten — nicht ihre Höhe, sondern ihre Dynamik. In den nächsten zwanzig Minuten zeige ich Ihnen, dass sich diese Dynamik systematisch unterscheidet, wie die Kennzahlen dabei zusammenhängen — und warum sich gut erklären lässt, wie stark ein Unternehmen schwankt, aber kaum, wie schnell es korrigiert."

*(Der letzte Halbsatz teasert den Hauptbefund an — die Prüfer wissen von Minute eins, worauf der Vortrag zuläuft. Anredeformen vorab prüfen.)*

### Seite 2 — Einleitung: Dynamik, φ & σ (1:15) · fertig

**Redetext:**
„Der Ausgangspunkt ist eine einfache Beobachtung: Eine Kennzahl wie der ROA ist eine Momentaufnahme. Ob zwölf Prozent Rendite belastbar oder fragil sind, verrät erst die Bewegung dahinter: Kehrt eine Veränderung im nächsten Quartal zurück — oder bleibt sie? Und wie stark schwankt die Kennzahl überhaupt? Genau diese beiden Dimensionen fasse ich als Dynamik: die Korrekturgeschwindigkeit φ — kehrt eine Quartalsveränderung im Folgequartal zurück? — und die Veränderungsvolatilität σ — wie groß sind die typischen Quartalsschwankungen? Diese Perspektive ist praktisch relevant: Wer eine Kennzahl fortschreiben, einen Ausschlag bewerten oder die Wirkung eines disruptiven Ereignisses einschätzen will, braucht genau diese beiden Informationen."

### Seite 3 — Forschungsfragen + Beitrag (1:15) · fertig

**Redetext:**
„Daraus ergeben sich meine drei Forschungsfragen. Erstens: Weisen Finanzkennzahlen über Unternehmen hinweg systematische Unterschiede in ihrer zeitlichen Dynamik auf? Zweitens: Welche Interdependenzen bestehen zwischen den Kennzahlen — und wie unterscheiden sich diese zwischen Unternehmen, auch über die Zeit und in Krisenphasen? Drittens: Stehen diese Dynamiken in Zusammenhang mit strukturellen Unternehmensmerkmalen?
Der Forschungsbeitrag liegt in drei Punkten: Ich übertrage die Mean-Reversion-Forschung in der Tradition von Fama und French von Jahres- auf Quartalsfrequenz und von gepoolten auf individuelle Schätzungen pro Unternehmen. Ich betrachte Korrekturgeschwindigkeit und Volatilität parallel über sieben Kennzahlen — als zweidimensionale Taxonomie auf Firmenebene. Und ich prüfe systematisch, welche der beiden Dimensionen sich strukturell erklären lässt."

### Seite 4 — Daten: Filterkette (1:00) · fertig, Redetext straffen

Die Tabelle bleibt als Beleg auf der Folie, wird aber nicht mehr durcherzählt — Details sind Backup B2.

**Redetext:**
„Zur Datenbasis, bewusst kompakt: Quartalsabschlüsse US-amerikanischer börsennotierter Unternehmen über 25 Jahre — 100 Quartale von 2000 bis 2024. Aus knapp 5.900 Unternehmen wird über die Filterkette die finale Stichprobe von 932: Finanzsektor ausgeschlossen, ADRs entfernt, Vollständigkeit über alle 100 Quartale, Ausreißerkorrektur und Winsorisierung. Ein Punkt verdient Ehrlichkeit: Der Vollständigkeitsfilter entfernt 77 Prozent der Unternehmen und erzeugt einen Survivorship Bias — ich habe ihn quantifiziert und getestet, dazu am Ende mehr. Mit sieben Kennzahlen aus Profitabilität, Liquidität und Kapitalstruktur ergeben sich 6.521 Unternehmen-Kennzahl-Kombinationen."

### Seite 5 — Methodik: AR(1) + Intuitionsgrafik G1 (1:45) · in Arbeit

**Folie:** Gleichung oben (hast du), darunter **G1**: drei simulierte Pfade nebeneinander. Morph-Idee: Die Gleichung bleibt stehen, die drei Panels erscheinen als Build.

**Redetext:**
„Für jede dieser 6.521 Kombinationen schätze ich ein eigenes AR(1)-Modell — nicht auf den Niveaus, sondern auf den ersten Differenzen, den Quartalsveränderungen. Drei Gründe: Die Veränderung hat eine direkte ökonomische Bedeutung, die Differenzenbildung sichert Stationarität ohne Annahmen über die Niveaus, und die einheitliche Transformation macht alle sieben Kennzahlen vergleichbar. φ misst damit die Autokorrelation der Veränderungen — nicht die Persistenz der Niveaus; auf diese Abgrenzung komme ich gleich noch einmal zurück.
Was der Koeffizient bedeutet, zeigen diese drei simulierten Pfade. Links φ gleich minus 0,45: Ein Ausschlag wird im Folgequartal fast zur Hälfte zurückgenommen — die Reihe pendelt eng um ihren Pfad, das ist Mean-Reversion. In der Mitte φ gleich null: Jede Veränderung ist von der vorherigen unabhängig — keine Vorhersagekraft. Rechts ein positives φ: Bewegungen setzen sich fort, die Reihe driftet. Geschätzt wird individuell per OLS — der Mean-Group-Ansatz nach Pesaran und Smith: keine gepoolte Zahl, sondern die volle Verteilung über 932 Unternehmen."

### Seite 6 — Methodik: Quadranten als φ-σ-Bühne (1:15) · in Arbeit

**Folie:** Leerer φ-σ-Raum, ein einzelner Beispielpunkt, dann Median-Linien als Build, vier Quadrantenlabels. Deine drei Nummern-Schritte passen. Wichtig für den Morph: Achsen und Medianlinien als **eigenständige, benannte Objekte** anlegen — sie leben auf Seite 7 weiter.

**Redetext:**
„Damit hat jedes Unternehmen pro Kennzahl zwei Koordinaten — und wird in diesem Raum zu einem Punkt: horizontal die Korrekturgeschwindigkeit, vertikal die Volatilität. Ein Median-Split in beiden Dimensionen erzeugt vier Dynamiktypen: korrektiv-stabil — kleine Ausschläge, die sich zurückbilden, die höchste Vorhersagbarkeit. Korrektiv-volatil — große Ausschläge mit schneller Korrektur. Persistent-stabil — träger Drift. Und persistent-volatil — große Ausschläge ohne Korrektur, das höchste Risikoprofil. Die Logik schließt an die Portfolio-Sorts von Fama und French an, die Labels sind direkt interpretierbar. Und wichtig: Die beiden Achsen tragen tatsächlich unabhängige Information — ihre gemeinsame Variation liegt selbst im stärksten Fall bei nur sechs Prozent."

### Seite 7 — FF1: Drei Dynamiktypen (2:00) · neu bauen

**Folie:** Der Raum von Seite 6 füllt sich per Morph mit allen Punkten — dafür **G4** (das Streudiagramm im Dark-Design neu gerendert). Rechts die drei Mediane als große Zahlen im Farbcode. Titel als Aussage: „Drei Dynamiktypen — Profitabilität korrigiert, Kapitalstruktur driftet".

**Redetext:**
„Jetzt füllt sich dieser Raum mit allen 6.521 Schätzungen — und damit sind wir bei den Ergebnissen. Es bilden sich drei klar getrennte Schichten, entlang der Kennzahlgruppen. Die Profitabilität — ROA, ROE, EBIT- und FCF-Marge — revertiert stark: φ-Mediane zwischen minus 0,43 und minus 0,46, bemerkenswert einheitlich über alle vier Kennzahlen. Über 90 Prozent der Einzelschätzungen sind signifikant, selbst nach Bonferroni-Korrektur bleiben rund 60 Prozent. Eine ROA-Veränderung wird im Median also zu 43 Prozent im Folgequartal korrigiert. Die Liquidität liegt mit minus 0,17 dazwischen — bei der höchsten Volatilität der gesamten Stichprobe. Und die Kapitalstruktur liegt nahe null: minus 0,04 bis minus 0,09; rund ein Drittel der Unternehmen zeigt hier gar keine Korrektur.
Interessant ist auch, was mit den wenigen positiven φ-Werten passiert: Ich habe sie gezielt geprüft — ihre Modellgüte liegt nahe null, kein einziger ist nach Bonferroni signifikant. Das sind Modellartefakte, keine eigene Dynamikklasse. Und die Rangfolge ist robust: über vier alternative Spezifikationen, vier Stichprobenschwellen und vier Zeitfenster bewegen sich die Mediane um höchstens ein bis zwei Hundertstel. Die Antwort auf Forschungsfrage eins: Ja — Finanzkennzahlen unterscheiden sich systematisch in ihrer Dynamik, und die Unterschiede folgen den Kennzahlgruppen."

### Seite 8 — FF1: Warum? (1:45) · Platzhalter überarbeiten

**Folie:** Strom/Bestand-Skizze (Abb. 15, idealerweise im Dark-Design nachgebaut — sie ist simpel genug, um sie nativ in PowerPoint als morphbare Objekte zu bauen: eine Achse, sieben Punkte, zwei Beschriftungspole) plus die zwei Karten „Markt korrigiert" / „Management entscheidet".

**Redetext:**
„Warum ist das so? Zwei Mechanismen erklären die Hierarchie. Erstens die Konstruktion der Kennzahlen: Stromgrößen wie die FCF- und die EBIT-Marge entstehen jedes Quartal neu — sie korrigieren am stärksten; die FCF-Marge sogar noch stärker als die EBIT-Marge, weil ihr keine Periodenabgrenzung die Ausschläge glättet. Reine Bestandsgrößen wie Eigenkapitalquote und Debt/Equity ändern sich nur durch Geschäftsvorfälle — sie korrigieren kaum. ROA, ROE und Current Ratio liegen als Mischformen dazwischen, exakt in der Reihenfolge ihres Bestandsanteils.
Zweitens der Korrekturmechanismus: Die Profitabilität korrigiert der Markt — eine überdurchschnittliche Marge zieht Wettbewerber an, eine unterdurchschnittliche erzwingt Kostenanpassung oder Marktaustritt. Das geschieht ohne Zutun des Unternehmens, und die Größenordnung passt zu Fama und French, die auf Jahresdaten rund 38 Prozent Reversion messen. Die Kapitalstruktur dagegen korrigiert sich nicht von selbst: Sie ändert sich nur, wenn das Management handelt — Emission, Rückkauf, Dividende. Pecking-Order-, Market-Timing- und Trade-off-Theorie begründen alle dieselbe Trägheit. Kurz: Der Markt korrigiert, das Management entscheidet — und dazwischen liegt die Liquidität."

### Seite 9 — NEU: Benchmark-Einordnung (1:15) · neu bauen (G2)

**Folie:** Die Benchmark-Achse (G2). Titel: „Nicht das Niveau zählt — die Spreizung". Morph-Idee: Die farbigen Median-Punkte kommen sichtbar aus dem Streudiagramm von Seite 7 „heruntergefallen" auf eine horizontale Achse; bei φ = −0,5 eine gestrichelte Linie mit Label „mechanische Grenze: Differenzen von weißem Rauschen".

**Warum diese Seite Gold wert ist:** Sie beantwortet Prof. Stollhoffs wahrscheinlichste Frage, bevor er sie stellt, und sie ist dein sichtbarster Beleg für „über die Arbeit hinaus weitergedacht".

**Redetext:**
„Einen Punkt möchte ich schärfer einordnen, als es die Arbeit selbst tut — er ist mir bei der weiteren Beschäftigung mit dem Thema wichtig geworden. Wer eine Zeitreihe differenziert, deren Niveaus unkorreliert sind, erhält rein mechanisch ein φ von minus 0,5 — das ist eine Eigenschaft der Differenzenbildung, nicht der Ökonomie. Diese Grenze habe ich hier markiert. Meine Profitabilitätswerte liegen in ihrer Nähe — das absolute Niveau ist also mit Vorsicht zu lesen. Entscheidend ist deshalb die Spreizung: Wäre alles Mechanik, müssten alle sieben Kennzahlen an dieser Linie liegen. Tatsächlich liegt die Kapitalstruktur bei nahe null und die Liquidität bei minus 0,17 — unter identischer Transformation. Diese Unterschiede sind Ökonomie. Genau deshalb interpretiere ich in der Arbeit durchgängig die Relationen zwischen den Kennzahlen, nicht die absoluten Niveaus."

### Seite 10 — FF2: Matrizen-Kontrast (1:30) · Platzhalter überarbeiten

**Folie:** Dein Layout mit den zwei großen Zählern (9/21 vs. 19/21) trägt bereits. Kür: Matrizen im Dark-Design neu rendern (G4-Kür). Titel als Aussage behalten.

**Redetext:**
„Forschungsfrage zwei: Wie hängen die Dynamiken zusammen? Dafür korreliere ich die geschätzten Parameter paarweise über die 932 Unternehmen — einmal für φ, einmal für σ, jeweils 21 Kennzahlpaare. Der Kontrast ist das Ergebnis. In der φ-Matrix sind nur 9 von 21 Paaren signifikant, und die starken Kopplungen liegen ausschließlich innerhalb der Profitabilität — ROA und ROE mit 0,78: Wer in einer Profitabilitätskennzahl schnell korrigiert, tut es auch in den anderen. Eine Ausnahme fällt auf: Die FCF-Marge koppelt nur lose an die Buchgewinne — das ist die Accrual-Mechanik nach Sloan und Dechow: Periodenabgrenzungen glätten Buchgewinne, den Cashflow nicht.
Die σ-Matrix dagegen ist mit 19 von 21 signifikanten Paaren fast vollständig verbunden. Mein Kernsatz: Schocks treffen die Kennzahlen gemeinsam — korrigiert werden sie kennzahlspezifisch. Und wichtig für die Sauberkeit: Kopplungen wie ROE mit Debt/Equity folgen aus der DuPont-Identität — solche mechanischen Verbindungen weise ich explizit aus und zähle sie nicht als ökonomischen Befund."

### Seite 11 — FF2: Krisenphasen (1:15) · Platzhalter überarbeiten

**Folie:** Deine Balken-/Jahreslogik (2001 · 2009 · 2020) funktioniert. Ergänzung als Kür: die rollierende Volatilitäts-Zeitreihe im Dark-Design (G4-Kür) statt abstrakter Balken.

**Redetext:**
„Zur zeitlichen Dimension: Krisen identifiziere ich datengetrieben — ein Quartal gilt als Hochvolatilitätsphase, wenn mindestens drei der sieben Kennzahlen über dem 90. Perzentil ihrer eigenen Volatilität liegen. Ohne jede Vorgabe findet dieses Kriterium genau drei Phasen: Dot-Com, die globale Finanzkrise und COVID — das stützt die Plausibilität des Verfahrens. In der Finanzkrise und in COVID trennt meine Quadranten-Klassifikation das Reaktionsverhalten signifikant: Volatil klassifizierte Unternehmen reagieren substanziell stärker, mit Effektstärken bis minus 0,36. Die Dot-Com-Phase trennt nicht — als sektorspezifische Tech-Krise mit geringer Querschnittsbreite ist genau das konsistent. Eine Einschränkung benenne ich selbst: Die Klassifikation stammt aus demselben Zeitraum — das ist eine In-Sample-Konsistenzprüfung, keine Out-of-Sample-Prognose."

### Seite 12 — FF3: Asymmetrie + Restinformation (2:00) · neu bauen (G3)

**Folie:** Dein 30 %/5 %-Layout mit den Exposition/Reaktion-Karten bleibt der Kern. Neuer Build (Morph): darunter erscheint das ΔR²-Ergebnis aus G3 als schmale Balkenreihe. Titel bleibt: „Struktur erklärt σ — nicht φ".

**Redetext:**
„Damit zum Hauptbefund, Forschungsfrage drei. Ich regressiere φ und σ pro Kennzahl auf fünf Strukturvariablen: Größe, Anlagenintensität, Investitionsintensität, Profitabilitätsniveau und Periodenabgrenzungen. Das Ergebnis ist eine klare Asymmetrie. Die Strukturvariablen erklären im Mittel rund 30 Prozent der Volatilität — bei der FCF-Marge fast die Hälfte. Von der Korrekturgeschwindigkeit erklären dieselben Variablen nur rund fünf Prozent — und das, obwohl bei 932 Unternehmen selbst kleine Effekte signifikant werden; an Teststärke liegt es also nicht. Meine Interpretation: σ misst Exposition — was ein Unternehmen ist, seine Größe, seine Bilanzstruktur, sein Geschäftsmodell, bestimmt, wie groß die Schocks sind, die es treffen. φ misst Reaktion — wie schnell korrigiert wird, ist wettbewerbs- und verhaltensgetrieben und bleibt idiosynkratisch. Das schließt den Bogen zur Markt-versus-Management-Logik von vorhin.
Ich habe diese Frage nach Abgabe der Arbeit noch einen Schritt weitergetrieben: Trägt die Dynamik-Klassifikation selbst Information über die Strukturmerkmale hinaus? Dazu habe ich die Quadranten-Zuordnung der ROA-Dynamik als zusätzliche Kontrollvariable in die Regressionen der übrigen Kennzahlen aufgenommen. Das Ergebnis: [ΔR²-Werte aus G3 eintragen]. Die Taxonomie trägt genau die Information, die Strukturmerkmale nicht erfassen — φ ist damit nicht nur unerklärt, sondern ein eigenständiges Firmenmerkmal."

### Seite 13 — Limitationen (1:15) · Platzhalter überarbeiten

**Folie:** Deine 4-Karten-Struktur passt. Tippfehler korrigieren: „AUSBLCK" → Ausblick-Zeile hier ganz streichen (der Ausblick gehört jetzt auf Seite 14).

**Redetext:**
„Vier Grenzen benenne ich selbst — jede mit ihrem Test. Erstens der Survivorship Bias: 77 Prozent Ausschluss durch den Vollständigkeitsfilter. Geprüft mit vier abgesenkten Schwellen bis hinunter zu 40 Quartalen und 2.356 Unternehmen — die φ-Mediane bleiben praktisch identisch. Zweitens die Differenzen-Konvention, die Sie eben gesehen haben: φ misst Veränderungs-Autokorrelation; ich interpretiere deshalb Relationen, nicht Niveaus. Drittens der In-Sample-Charakter der Krisentests — deklariert als Konsistenzprüfung; der Out-of-Sample-Test ist der logische nächste Schritt. Und viertens der Geltungsbereich: etablierte US-Unternehmen auf Quartalsfrequenz — junge Unternehmen, Effekte unterhalb eines Quartals und andere Märkte bleiben offen."

### Seite 14 — Fazit: Der Rahmen schließt sich (2:00) · neu bauen

**Folie:** Die drei FF-Karten von Seite 3 kehren per Morph zurück (identische Objekte kopieren, damit Morph sie erkennt), jede bekommt eine Antwortzeile im Farbcode angeheftet. Darunter eine schmale Ausblick-Zeile und der Dank. Kein neues Bildmaterial nötig.

**Redetext:**
„Ich komme zum Fazit — und dafür kehren die drei Fragen vom Anfang zurück, jetzt mit ihren Antworten. Erstens: Ja — Finanzkennzahlen unterscheiden sich systematisch in ihrer Dynamik. Es gibt drei Dynamiktypen entlang der Kennzahlgruppen: Profitabilität korrigiert stark, Liquidität moderat, Kapitalstruktur driftet. Zweitens: Volatilität ist eine gekoppelte Unternehmenseigenschaft — Schocks treffen die Kennzahlen gemeinsam; die Korrekturgeschwindigkeit dagegen bleibt kennzahlspezifisch, und in zwei von drei Krisen trennt die Taxonomie das Reaktionsverhalten. Drittens: Strukturmerkmale erklären rund 30 Prozent der Volatilität, aber nur fünf Prozent der Korrekturgeschwindigkeit — φ ist ein idiosynkratisches Firmenmerkmal.
Was heißt das praktisch? Zwei Beispiele: Wer eine Profitabilitätsveränderung fortschreibt, sollte im Median 43 Prozent Gegenbewegung im Folgequartal einpreisen. Und wer darauf wartet, dass eine Verschuldungsquote von selbst zur Norm zurückkehrt, wartet vergeblich — solange das Management nicht handelt.
Für die Forschung ergeben sich vier Anschlusslinien: der Out-of-Sample-Test der Quadranten, die Lead-Lag-Analyse auf AR-Residuen, höhere Datenfrequenz und Märkte jenseits der USA. Vielen Dank — ich freue mich auf Ihre Fragen."

---

## Grafik-Produktionsliste (Priorität in dieser Reihenfolge)

**G2 — Benchmark-Achse (Seite 9) · ~1 h · nativ in PowerPoint (morphbar).**
Horizontale Linie als φ-Achse von −0,6 bis +0,1. Gestrichelte Vertikale bei −0,5, Label „mechanische Grenze: Differenzen von weißem Rauschen"; zweite dezente Markierung bei 0. Sieben Punkte: ROA −0,431, ROE −0,427, EBIT −0,431, FCF −0,459 (Blau `78A2F9`, eng gebündelt — vertikal leicht versetzen und mit kleinen Labels), Current Ratio −0,174 (Gelb `E6D44F`), Debt/Equity −0,089 und EK-Quote −0,040 (Koralle `E8867C`). Als PowerPoint-Formen bauen, nicht als Bild — dann können die Punkte per Morph von Seite 7 „herunterfallen".

**G1 — Intuitionsgrafik (Seite 5) · ~1–2 h · Python/matplotlib.**
Drei Panels nebeneinander, je ~60 simulierte Quartale: `x[t] = phi*x[t-1] + e[t]`, gleiche Fehler (seed fixieren!), phi ∈ {−0,45; 0; +0,3}, identische y-Skala. Dark-Design: `fig`/`axes` facecolor `#1E402E`, Achsen/Ticks/Labels `#F2EFDA`, Linienfarben Blau/Sage/Gelb, dünne Nulllinie. Paneltitel: „φ = −0,45 · korrektiv" / „φ = 0 · unkorreliert" / „φ = +0,3 · persistent". Export PNG 300 dpi.

**G3 — Restinformations-Analyse (Seite 12 + Backup B4) · ~½ Tag · Python.**
⚠️ **Zirkularitäts-Falle vermeiden:** Nicht die Quadranten der Kennzahl X zur Erklärung von φ/σ derselben Kennzahl X verwenden — die Dummies stammen aus deren eigenem Median-Split, das ΔR² wäre per Konstruktion hoch und im Kolloquium sofort angreifbar. **Saubere Variante:** Quadranten-Zuordnung einer Referenzkennzahl (ROA) als kategorialer Prädiktor für die übrigen sechs Kennzahlen. Ablauf pro Kennzahl k ≠ ROA und pro Parameter (φ, σ): M0 = OLS auf die fünf Strukturvariablen (Größenmaße logarithmiert); M1 = M0 + drei Dummies (K-V, P-S, P-V; Basis K-S) der ROA-Quadranten; berichte ΔR² = R²(M1) − R²(M0). Darstellung: Balkenreihe ΔR² pro Kennzahl, zwei Panels (φ/σ), Dark-Design wie G1. Erwartung: bei φ spürbar, bei σ klein — exakt die Story von Seite 12. Werte in den Redetext-Platzhalter eintragen.

**G4 — Dark-Render der Ergebnisgrafiken · Pflicht: FF1-Streudiagramm (~1–2 h); Kür: Matrizen, Volatilitäts-Zeitreihe.**
FF1-Streudiagramm als Pendant zu Abbildung 4 mit deiner Palette neu rendern: Hintergrund `#1E402E`, Punkte alpha ≈ 0,35 in Blau/Gelb/Koralle, Median-Linien gestrichelt `#F2EFDA`, log-Skala auf σ beibehalten, Randbox-Plots optional weglassen (die Folie braucht die Schichten, nicht jedes Detail).

**G5 — Kür (nur falls am Samstag noch Luft ist): Out-of-Sample-Teaser.**
Quadranten aus 2000–2019 schätzen, |ΔY| in 2020Q2/Q3 zwischen volatil/stabil vergleichen (Mann-Whitney, r_rb). Als Backup-Folie „Out-of-Sample-Vorschau" — das stärkste denkbare „weitergearbeitet"-Signal, aber verzichtbar.

---

## Backup-Folien (nummeriert, nie ungefragt zeigen)

B1 Validierung (deine bisherige Folie 13 unverändert verschieben) · B2 Filterkette im Detail (Tabelle) · B3 Robustheit (Spezifikationen + Stichprobenschwellen) · B4 Restinformation im Detail (G3) · B5 Beispielfirmen MGEE/Walmart/TXN · B6 Out-of-Sample (falls G5) · B7 Errata-Liste.

---

## 5-Tage-Plan

**Do 02.07. (heute):** Struktur übernehmen (Validierung → B1, Seite 9 und 14 anlegen), G2 nativ bauen, G1 rechnen, Methodik-Seiten 5–6 fertigstellen.
**Fr 03.07.:** G3 rechnen und Werte in Seite 12 + Redetext eintragen, G4-Pflicht rendern, Seiten 7–14 bauen, kompletten Redetext in die PPT-Notizen übernehmen.
**Sa 04.07.:** Zwei laute Durchläufe mit Stoppuhr (Ziel 19:00–19:45). Nach dem ersten: kürzen, wo es hakt — gekürzt wird im Redetext, nie an den Kernzahlen.
**So 05.07.:** Generalprobe vor Publikum oder Kamera. Danach Fragen-Drill: die zwölf Fragen aus dem Verteidigungsplan, jede Antwort unter 90 Sekunden. Backups und Errata finalisieren.
**Mo 06.07.:** Nur Feinschliff. Technik-Check — Achtung: **ein PDF-Fallback verliert alle Morph-Übergänge**; eigener Laptop plus Adapter ist Pflicht, PDF nur als Notnagel. Zahlen-Spickzettel wiederholen, früh schlafen.
**Di 07.07.:** Kolloquium. Der erste Satz sitzt auswendig — der Rest läuft.
