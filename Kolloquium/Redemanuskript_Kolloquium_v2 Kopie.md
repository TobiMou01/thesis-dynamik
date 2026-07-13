# Redemanuskript Kolloquium — v2 (Stand 04.07.2026)

**Basis:** aktuelles Deck (26 Folien, Stand 04.07.) + Master-Briefing. Gesamtzeit **≈ 19:30** bei ruhigem Tempo (~110 Wörter/Minute). Klick-Marken **(→ Klick)** zeigen die Builds innerhalb einer logischen Seite.

**Drei Sprechgrundsätze** (aus dem Briefing destilliert): Erstens ergebnisgetrieben — die Methode trägt der Sprechtext, die Folie zeigt den Befund. Zweitens kurze Sätze, jede Zahl bekommt einen Halbsatz Bedeutung. Drittens Schwächen selbst benennen, bevor sie gefragt werden — aber als getestete Grenzen, nie als Entschuldigung.

| Block | Folien | Zeit |
|---|---|---|
| Einstieg + Methodik | 01–05 | 4:15 |
| FF1 | 06–08 | 4:10 |
| FF2 | 09–11 | 4:45 |
| FF3 | 12–14 | 4:00 |
| Limitationen + Fazit | 15 + (16) | 2:00 |

---

## Folie 01 — Titel (0:30)

„Sehr geehrter Herr Professor Steglich, sehr geehrter Herr Professor Stollhoff, vielen Dank für die Gelegenheit, meine Masterarbeit zu verteidigen. Ich habe untersucht, wie sich Finanzkennzahlen börsennotierter US-Unternehmen über die Zeit verhalten — nicht ihre Höhe, sondern ihre Dynamik. Die Arbeit steht in der Tradition der Mean-Reversion-Forschung von Fama und French und nutzt den Mean-Group-Gedanken von Pesaran und Smith — und sie überträgt beides dorthin, wo es bisher nicht angewendet wurde: auf Quartalsfrequenz und auf das einzelne Unternehmen. In den nächsten zwanzig Minuten zeige ich Ihnen, dass sich diese Dynamik systematisch unterscheidet — und warum sich gut erklären lässt, wie stark ein Unternehmen schwankt, aber kaum, wie schnell es korrigiert."

*Der letzte Satz teasert den Hauptbefund — die Prüfer wissen ab Minute eins, worauf der Vortrag zuläuft. Auswendig sprechen.*

## Folie 02 — Einleitung: Dynamik, φ & σ (1:15)

„Der Ausgangspunkt steht als Satz auf der Folie: Eine Kennzahl ist eine Momentaufnahme — die Information steckt in der Veränderung. Ob zwölf Prozent Rendite belastbar oder fragil sind, verrät erst die Bewegung dahinter. Diese Bewegung fasse ich in zwei Größen: die Korrekturgeschwindigkeit φ — kehrt eine Quartalsveränderung im Folgequartal zurück? — und die Veränderungsvolatilität σ — wie groß sind die typischen Ausschläge? Mit genau dieser Definition von Dynamik beantworte ich alle drei Forschungsfragen."

**(→ Klick: Forschungsfragen + Beitrag)**

„Erstens: Unterscheiden sich Finanzkennzahlen systematisch in ihrer zeitlichen Dynamik? Zweitens: Welche Interdependenzen bestehen zwischen den Kennzahlen — im Querschnitt, über die Zeit und in Krisenphasen? Drittens: Hängen diese Dynamiken mit strukturellen Unternehmensmerkmalen zusammen? Aus den Antworten entsteht der Beitrag der Arbeit: die Übertragung der Mean-Reversion-Forschung auf Quartalsfrequenz und individuelle Schätzungen, die parallele Behandlung von Korrekturgeschwindigkeit und Volatilität über sieben Kennzahlen als zweidimensionale Taxonomie — und die systematische Prüfung, welche der beiden Dimensionen sich strukturell erklären lässt."

## Folie 03 — Daten: Filterkette (0:40) · *bewusst kurz*

„Zur Datenbasis, bewusst kompakt: Quartalsabschlüsse US-amerikanischer börsennotierter Unternehmen — 100 Quartale, 2000 bis 2024. Die Filterkette reduziert knapp 5.900 Unternehmen auf 932: Finanzsektor ausgeschlossen, ADRs entfernt, Vollständigkeit über alle 100 Quartale, Ausreißerbehandlung, Winsorisierung. Ein Punkt verdient Ehrlichkeit: Der Vollständigkeitsfilter entfernt 77 Prozent der Unternehmen — diesen Survivorship Bias habe ich quantifiziert und getestet, dazu am Ende mehr. Es bleiben 6.521 Unternehmen-Kennzahl-Zeitreihen über sieben Kennzahlen aus Profitabilität, Liquidität und Kapitalstruktur."

## Folie 04 — AR(1) auf ersten Differenzen (0:50)

„Für jede dieser 6.521 Zeitreihen schätze ich ein eigenes AR(1)-Modell — nicht auf den Niveaus, sondern auf den ersten Differenzen, den Quartalsveränderungen. Die Gleichung lesen Sie so: Die heutige Veränderung ergibt sich aus einer Konstante c, dem φ-fachen der Vorquartalsveränderung und einem Störterm — und die Standardabweichung dieses Störterms ist mein σ. Drei Gründe für die Differenzen: Die Veränderung hat eine direkte ökonomische Bedeutung, die Differenzenbildung sichert Stationarität ohne Annahmen über die Niveaus, und die einheitliche Transformation macht alle sieben Kennzahlen vergleichbar. φ misst damit die Autokorrelation der Veränderungen, nicht die Persistenz der Niveaus — auf diese Abgrenzung komme ich bei den Grenzen der Arbeit zurück. Geschätzt wird individuell per OLS — der Mean-Group-Ansatz nach Pesaran und Smith: keine gepoolte Zahl, sondern die volle Verteilung über 932 Unternehmen."

## Folie 05 — Quadranten: die φ-σ-Bühne (1:00)

„Damit hat jedes Unternehmen pro Kennzahl zwei Koordinaten — und wird in diesem Raum zu einem Punkt. Ein Median-Split in beiden Dimensionen erzeugt vier Dynamiktypen: korrektiv-stabil — kleine Ausschläge, die sich zurückbilden, die höchste Vorhersagbarkeit. Korrektiv-volatil — große Ausschläge mit schneller Korrektur. Persistent-stabil — träger Drift. Und persistent-volatil — große Ausschläge ohne Korrektur, das höchste Risikoprofil. Drei Dinge machen diese Klassifikation stark: Sie schließt an die Portfolio-Sort-Logik von Fama und French an, die Labels sind ohne Umweg interpretierbar, und die beiden Achsen tragen nachweislich unabhängige Information — ihre gemeinsame Variation liegt selbst im stärksten Fall bei nur sechs Prozent. Behalten Sie diesen Raum im Kopf — er füllt sich jetzt mit Ergebnissen."

*Übergang ist der Anlauf auf FF1 — kurze Pause nach diesem Satz.*

---

## Folie 06 — FF1 · Drei Dynamiktypen (1:50)

„Und er füllt sich mit einem klaren Muster: drei getrennte Dynamiktypen, exakt entlang der Kennzahlgruppen. Die Profitabilität revertiert stark — φ-Mediane zwischen minus 0,43 und minus 0,46, über vier völlig verschieden konstruierte Kennzahlen hinweg fast identisch. Was nicht auf der Folie steht: Die vier Verteilungen liegen praktisch deckungsgleich übereinander, und weniger als zwei Prozent der Schätzungen sind überhaupt positiv — diese Mean-Reversion ist kein Mittelwertsphänomen, sie gilt in der Breite der Stichprobe. Eine ROA-Veränderung wird im Median zu 43 Prozent im Folgequartal korrigiert. Die Liquidität liegt mit minus 0,17 dazwischen — bei der höchsten Volatilität der gesamten Stichprobe. Und die Kapitalstruktur liegt nahe null — rund ein Drittel der Unternehmen zeigt dort gar keine Korrektur. Zweiter Blick hinter die Folie: Auf der σ-Achse sortieren sich die Kennzahlen nach ihrer Bezugsbasis — ROA mit der großen Bilanzsumme im Nenner ist am ruhigsten, die FCF-Marge im Median zehnmal so volatil; je näher an Umsatz und Cashflow, desto größer die Ausschläge. Und die Rangfolge ist robust: vier Modellspezifikationen, vier Stichprobenschwellen, vier Zeitfenster — die Mediane bewegen sich um höchstens ein bis zwei Hundertstel."

**(→ Klick: Schätzqualitäts-Leiste)**

„Die Schätzqualität folgt derselben Hierarchie — und das ist selbst ein Befund. In der Profitabilität sind über 90 Prozent der Schätzungen signifikant, nach Bonferroni bleiben rund 60 Prozent. In der Kapitalstruktur sind es nur noch 19 bis 32 Prozent — und das ist kein Schwachpunkt des Modells, das ist die Antwort: Die Bilanzstruktur folgt keinem stetigen Korrekturprozess, sie bewegt sich in diskreten Managemententscheidungen. Die positiven φ-Werte habe ich gezielt geprüft: Modellgüte nahe null, kein einziger nach Bonferroni signifikant — Modellartefakte, keine eigene Dynamikklasse. Und ein Muster, das später wichtig wird: Volatile Firmen revertieren stärker und werden vom Modell deutlich besser erkannt."

## Folie 07 — FF1 · Analyse nach Sektor (1:15)

„Jetzt die Gegenprobe — und sie hat mich selbst überrascht. Die Erwartung wäre: Die Branche dominiert die Dynamik, Technologie tickt anders als Versorger. Die Daten sagen etwas anderes. Innerhalb der Profitabilität liegen alle zehn Sektor-Mediane in einem Band von nur 0,12 — sobald die Kennzahl feststeht, rücken die Sektoren eng zusammen. Die Kennzahl prägt die Dynamik stärker als der Sektor: Wer die Dynamik verstehen will, muss zuerst auf die Konstruktion der Kennzahl schauen, nicht auf die Branche. Und die Ausnahmen bestätigen den Mechanismus, statt ihn zu stören: In der Liquidität ist das Band doppelt so breit — Immobilien erreichen dort die 2,6-fache Volatilität, getrieben von REIT-Refinanzierungen, bei gleichzeitig stärkster Korrektur und bester Schätzqualität. Und in der Kapitalstruktur korrigiert ein einziger Sektor konsistent: die Versorger — genau dort, wo Regulierung die Anpassung erzwingt. Wo ein externer Mechanismus eingreift, verschiebt sich die Dynamik. Wo keiner eingreift, bleibt sie ein Merkmal der Kennzahl."

**(→ Klick: drei Sektor-Profile)**

„Verdichtet in die Quadranten ergeben sich drei Profile: das stabile — Versorger, Industrie, Basiskonsum. Das persistente — Technologie und Grundstoffe, wo Wachstums- und Rohstofftrends nachwirken. Und das korrektiv-volatile — Immobilien, Kommunikation, Energie. Fünf Sektoren bündeln sich in nur zwei Quadranten; einzig der zyklische Konsum streut über alle vier."

## Folie 08 — FF1 · Warum? (1:30) · *technisch tief — Kompetenzfolie*

„Warum ist das so? Zwei Mechanismen erklären die Hierarchie. Erstens die Konstruktion der Kennzahlen: Stromgrößen wie FCF- und EBIT-Marge entstehen jedes Quartal neu — sie korrigieren am stärksten; die FCF-Marge noch stärker als die EBIT-Marge, weil keine Periodenabgrenzung ihre Ausschläge glättet. Reine Bestandsgrößen wie Eigenkapitalquote und Debt/Equity ändern sich nur durch Geschäftsvorfälle — sie korrigieren kaum. ROA, ROE und Current Ratio liegen als Mischformen dazwischen, exakt in der Reihenfolge ihres Bestandsanteils. Zweitens der Korrekturmechanismus: Die Profitabilität korrigiert der Markt — Überrenditen ziehen Wettbewerber an, Unterrenditen erzwingen Kostenanpassung oder Marktaustritt. Das geschieht ohne Zutun des Unternehmens, und die Größenordnung passt zu Fama und French, die auf Jahresdaten rund 38 Prozent Reversion messen. Die Kapitalstruktur dagegen korrigiert sich nicht von selbst: Sie ändert sich nur, wenn das Management handelt — Emission, Rückkauf, Dividende. Pecking-Order-, Market-Timing- und Trade-off-Theorie begründen alle dieselbe Trägheit. Der Kernsatz meiner ersten Forschungsfrage: Der Markt korrigiert die Profitabilität — das Management entscheidet die Kapitalstruktur. Und dazwischen liegt die Liquidität."

### Optionaler Einschub „Benchmark-Einordnung" (1:00) — *falls die G2-Folie noch gebaut wird (Stollhoff-Folie aus dem Drehbuch)*

„Einen Punkt möchte ich schärfer einordnen, als es die Arbeit selbst tut. Wer eine Reihe differenziert, deren Niveaus unkorreliert sind, erhält rein mechanisch ein φ von minus 0,5 — eine Eigenschaft der Transformation, nicht der Ökonomie. Meine Profitabilitätswerte liegen in der Nähe dieser Grenze — das absolute Niveau ist also mit Vorsicht zu lesen. Entscheidend ist die Spreizung: Wäre alles Mechanik, müssten alle sieben Kennzahlen an dieser Linie liegen. Tatsächlich liegt die Kapitalstruktur bei null und die Liquidität bei minus 0,17 — unter identischer Transformation. Diese Unterschiede sind Ökonomie. Genau deshalb interpretiere ich durchgängig Relationen, nicht Niveaus."

---

## Folie 09 — FF2 · Querschnittliche Interdependenz (2:00)

„Forschungsfrage zwei: Hängen diese Dynamiken zusammen? Dafür korreliere ich die geschätzten Parameter paarweise über die 932 Unternehmen — Spearman-Rangkorrelation, 21 Kennzahlpaare je Matrix. Jede Zelle beantwortet eine präzise Frage: Wenn ein Unternehmen in Kennzahl A zu den schnellen Korrigierern gehört — gehört es dann auch in Kennzahl B dazu? In der φ-Matrix lautet die Antwort fast nur innerhalb der Profitabilität ja: ROA und ROE mit 0,78, mit der EBIT-Marge 0,56 und 0,54 — die Korrekturgeschwindigkeit ist dort ein konsistentes Firmenmerkmal. Die FCF-Marge fällt heraus: nur 0,14 bis 0,19 zu den Buchgewinnen — Periodenabgrenzungen glätten Buchgewinne, den Cashflow nicht, das ist die Accrual-Mechanik nach Sloan und Dechow. Merken Sie sich diese Sonderstellung, sie kehrt heute noch zweimal wieder. Und zwischen den Blöcken: ein einziges signifikantes Paar von zwölf."

**(→ Klick: σ-Matrix erscheint)**

„Jetzt dieselbe Rechnung, dieselben Firmen, dieselben 21 Paare — nur der Parameter wechselt von φ zu σ. Und das Bild kippt: 19 von 21 Paaren signifikant. Das ist der Kernbefund der zweiten Forschungsfrage: Schocks treffen die Kennzahlen gemeinsam — korrigiert werden sie kennzahlspezifisch. Die Eigenkapitalquote koppelt als einzige Kennzahl mit allen sechs anderen — die Bilanz spürt Gewinn- und Finanzierungsschocks gleichermaßen. Und für die Sauberkeit: ROE mal Debt/Equity mit 0,66 folgt aus der DuPont-Identität, EBIT mal FCF aus dem gemeinsamen Umsatznenner — mechanische Kopplungen, explizit ausgewiesen, nicht als Ökonomie verkauft."

**(→ Klick: untere Leiste φ×σ + Lead-Lag)**

„Zwei Ergänzungen schließen den Querschnitt: Innerhalb jeder Kennzahl korrelieren φ und σ schwach negativ — volatilere Firmen korrigieren schneller, das bestätigt Dichev und Tang. Aber alle Werte bleiben unter 0,25: Die Achsen sind trennbar, der Median-Split steht auf festem Boden. Und die Lead-Lag-Analyse liefert ein ehrliches Nullergebnis: 13 von 21 Paaren erreichen ihren Peak bei Lag null — Schocks laufen synchron; was sich innerhalb eines Quartals abspielt, kann Quartalsfrequenz nicht auflösen."

## Folie 10 — FF2 · Krisen + Sektor-Drift (1:30)

„Zur zeitlichen Dimension. Krisen definiere ich datengetrieben: Ein Quartal zählt als Hochvolatilitätsphase, wenn mindestens drei der sieben Kennzahlen über dem 90. Perzentil ihrer rollierenden Querschnittsvolatilität liegen. Elf Quartale erfüllen das Kriterium — und sie gruppieren sich ohne jede Vorgabe exakt in Dot-Com, Finanzkrise und COVID. Das stützt die Plausibilität des Verfahrens. COVID ist die stärkste Auslenkung: Peak 2020Q2, sechs von sieben Kennzahlen, mittleres Perzentil 99."

**(→ Klick: Sektor-Drift)**

„Vor den Krisentests der langfristige Trend — hier beschreibe ich kurz die Analyse: Pro Sektor und Kennzahl glätte ich das Median-Niveau über 25 Quartale und schätze parallel die AR(1)-Drift-Konstante c pro Unternehmen — zwei unabhängige Messungen desselben Trends, Übereinstimmung r gleich 0,86. Das Beispiel Technologie erzählt die klarste Geschichte: Die Current Ratio fällt von 2,48 auf 1,87, Debt/Equity steigt von 0,18 auf 0,42 — die Kurven kreuzen sich um 2013: der Übergang vom liquiditätsdominierten Start-up-Profil zur reifen, fremdfinanzierten Struktur. Und über alle 70 Sektor-Kennzahl-Kombinationen: Debt/Equity driftet in allen zehn Sektoren positiv, die Eigenkapitalquote in sieben von zehn negativ — die Verschuldungs- und Margenexpansion der letzten 25 Jahre, konsistent mit Bates und Graham."

## Folie 11 — FF2 · Quadranten-Reaktionen + Kennzahl-Signaturen (1:15)

„Jetzt die Krisentests: Trennt meine Klassifikation das Reaktionsverhalten? In der Finanzkrise deutlich: Effektstärke minus 0,36 für ROA und EBIT-Marge — volatil klassifizierte Unternehmen reagieren substanziell stärker. COVID bestätigt: minus 0,27, Kruskal-Wallis-Effektstärken bis 0,13. Dot-Com trennt nicht — als sektorspezifische Tech-Krise mit geringer Querschnittsbreite ist genau das konsistent. Die Testbilanz: sieben von zwölf Tests Bonferroni-signifikant, elf nach FDR. Und selbst benannt: Die Klassifikation stammt aus demselben Zeitraum — das ist eine In-Sample-Konsistenzprüfung, keine Prognose."

**(→ Klick: Chip-Reihe „Reaktion vs. Baseline")**

„Und jede Krise hat ihre Kennzahl-Signatur: Die EBIT-Marge reagiert in Finanzkrise und COVID am stärksten — Faktor 1,5 über der Baseline, der operative Hebel: Umsatz bricht, Kosten bleiben. Debt/Equity dagegen springt in der Dot-Com-Phase — der Kurs-Crash vernichtet Eigenkapital rein mechanisch. Die FCF-Marge bleibt in der Finanzkrise fast unauffällig — da ist sie wieder, die Sonderstellung aus der φ-Matrix. Und die Current Ratio reagiert überall am schwächsten — die träge Bilanzposition."

---

## Folie 12 — FF3 · Unternehmensmerkmale (1:15) · *Vorgehen zuerst, dann Muster*

„Forschungsfrage drei — und hier zuerst zum Vorgehen, bevor ich werte. Fünf Strukturvariablen: drei Größenmaße, die Anlagenintensität, die Investitionsintensität, das langfristige Profitabilitätsniveau und die Periodenabgrenzungen nach Sloan. Jede teste ich gegen φ und σ jeder Kennzahl — 98 paarweise Spearman-Tests, Bonferroni-korrigiert, ergänzt um Quintilvergleiche. Erst aus dieser Testfamilie ergibt sich das Muster: 31 von 49 σ-Tests signifikant, nur 10 von 49 bei φ — und die zehn stärksten Effekte betreffen ausnahmslos σ. Am stärksten wirkt die Größe: Die Mitarbeiterzahl dämpft die Volatilität von FCF-Marge und Current Ratio mit minus 0,53; vom kleinsten zum größten Quintil fällt der σ-Median von 0,45 auf 0,11 — der stärkste Effekt der gesamten Analyse. Und die Anlagenintensität zeigt das feinste Muster: Bilanzgrößen werden stabiler, reine Strom-Margen volatiler — die Strom-Bestand-Mechanik aus Forschungsfrage eins, wiedergefunden auf Unternehmensebene."

**(→ Klick: Profitabilitätsniveau + Accruals)**

„Zwei Variablen ergänzen das Bild: Profitable Unternehmen schwanken weniger — und revertieren sogar etwas langsamer: weniger Schwankung, weniger Korrekturbedarf. Und die Periodenabgrenzungen dämpfen die Volatilität der Buchgewinne, aber nicht die der FCF-Marge — damit ist der Mechanismus hinter der FCF-Sonderstellung aus Forschungsfrage zwei direkt nachgewiesen."

## Folie 13 — FF3 · Sektormerkmale (1:30) · *ergebnisgetrieben, nicht methodisch*

„Das kategoriale Gegenstück ist der Sektor — und die Antwort fällt gleich aus: Der Sektor erklärt die Schwankung, nicht die Korrektur. Auf der σ-Seite erklärt die Sektorzugehörigkeit bis zu 22 Prozent der Variation, FCF-Marge und Current Ratio vorn, alle sieben Kennzahlen signifikant. Auf der φ-Seite maximal sieben Prozent — dieselbe Asymmetrie wie bei den Strukturvariablen."

**(→ Klick: FinSrv-Karte)**

„Der schärfste Kontrast kommt von den 451 ausgeschlossenen Finanzdienstleistern, die ich parallel geschätzt habe: Current-Ratio-Volatilität beim 29-Fachen der Hauptstichprobe, ROA-Volatilität bei einem Fünftel — und die Bilanz-Kennzahlen revertieren deutlich stärker, weil regulatorische Mindestquoten die Korrektur erzwingen. Der Sektorausschluss ist damit empirisch begründet, nicht Konvention."

**(→ Klick: Cluster-Chips)**

„Und die härteste Prüfung: Aus jeder Sektor-Cluster-Mechanik von Forschungsfrage eins habe ich eine falsifizierbare Vorhersage zur Quadrantenverteilung abgeleitet. Drei von vier Clustern bestätigen sich mit 60 bis 66 Prozent Konformität. Das schwächste benenne ich offen: Kommunikation und Energie mit 43 Prozent — bei der FCF-Marge nur 30, weil Investitionszyklen den Cashflow länger als ein Quartal persistieren lassen. Und das fünfte Cluster bleibt diffus — genau wie vorhergesagt."

## Folie 14 — FF3 · Synthese: Struktur erklärt σ, nicht φ (1:15)

„Die multivariate Synthese bündelt alles: Pro Kennzahl und Parameter eine OLS-Regression mit allen fünf Strukturvariablen. Das Ergebnis ist die klarste Asymmetrie der Arbeit: Im Mittel erklären die Strukturvariablen 30 Prozent der Volatilität — bei der FCF-Marge 49 Prozent — aber nur fünf Prozent der Korrekturgeschwindigkeit. Und das, obwohl bei 932 Unternehmen selbst kleine Effekte signifikant werden — an Teststärke liegt es nicht. Meine Interpretation: σ misst Exposition — was ein Unternehmen ist, seine Größe, seine Bilanz, sein Geschäftsmodell, bestimmt, wie groß die Schocks sind, die es treffen. φ misst Reaktion — wie schnell korrigiert wird, ist wettbewerbs- und verhaltensgetrieben und bleibt idiosynkratisch. Das schließt den Bogen zur Markt-versus-Management-Logik vom Anfang. Und das So-what: Für Investoren — wer eine Profitabilitätsveränderung fortschreibt, sollte im Median 43 Prozent Gegenbewegung im Folgequartal einpreisen. Für die Kreditanalyse — eine Verschuldungsquote kehrt nicht von selbst zur Norm zurück: Covenants statt Vertrauen auf Reversion. Und fürs Risiko-Screening — die Struktur sagt Ihnen, wie stark ein Unternehmen schwankt; wie schnell es korrigiert, bleibt Sache des einzelnen Unternehmens."

---

## Folie 15 — Limitationen (0:50)

„Vier Grenzen benenne ich selbst — jede mit ihrem Test. Erstens der Survivorship Bias: 77 Prozent Ausschluss; geprüft mit vier abgesenkten Schwellen bis 40 Quartale und 2.356 Unternehmen — die φ-Mediane bleiben praktisch identisch. Zweitens die Differenzen-Konvention: φ misst Veränderungs-Autokorrelation, nicht Niveau-Persistenz — deshalb interpretiere ich Relationen, nicht Niveaus. Drittens der In-Sample-Charakter der Krisentests — deklariert als Konsistenzprüfung; der Out-of-Sample-Test ist der logische nächste Schritt. Viertens der Geltungsbereich: etablierte US-Unternehmen auf Quartalsfrequenz — junge Unternehmen, Effekte unterhalb eines Quartals und andere Märkte bleiben offen."

## Folie 16 — Fazit (1:10) · *Folie fehlt noch — FF-Karten kehren per Morph zurück*

„Ich komme zum Fazit — die drei Fragen vom Anfang, jetzt mit Antworten. Erstens: Ja — Finanzkennzahlen unterscheiden sich systematisch in ihrer Dynamik, in drei Dynamiktypen entlang der Kennzahlgruppen: Profitabilität korrigiert stark, Liquidität moderat, Kapitalstruktur driftet. Zweitens: Volatilität ist eine gekoppelte Unternehmenseigenschaft — Schocks treffen die Kennzahlen gemeinsam, korrigiert wird kennzahlspezifisch; in zwei von drei Krisen trennt die Taxonomie das Reaktionsverhalten. Drittens: Strukturmerkmale erklären rund 30 Prozent der Volatilität, aber nur fünf Prozent der Korrekturgeschwindigkeit — φ ist ein eigenständiges, idiosynkratisches Firmenmerkmal. Für die Forschung ergeben sich vier Anschlusslinien: der Out-of-Sample-Test der Quadranten, die Lead-Lag-Analyse auf AR-Residuen, höhere Datenfrequenz und Märkte jenseits der USA. Vielen Dank — ich freue mich auf Ihre Fragen."

---

# Anmerkungen zum Briefing (Abweichungen + offene Punkte)

**Stillschweigend korrigiert (Briefing = alter Stand, Arbeit ist verbindlich):**

1. **AR-Gleichung:** Das Briefing schreibt Y_t = c + φ·Y_{t−1} + ε_t (Niveaus). Die Arbeit schätzt auf **ersten Differenzen** (ΔY) — Deck und Redetext bleiben bei ΔY; das ist zugleich die Vorlage für die Differenzen-Konventions-Frage (Stollhoff).
2. **„Nur ca. 200 von 932 signifikant bei der Kapitalstruktur":** Tatsächlich Debt/Equity 32,4 % (~302 Firmen), EK-Quote 18,6 % (~173) bei p < 0,05 (Tabelle 8). Die offensive Argumentationslinie („kein stetiger AR-Prozess, sondern diskrete Management-Schocks") bleibt voll gültig und steckt jetzt in Folie 06, Build 2.
3. **Kruskal-Wallis-Folie:** Liegt inhaltlich in FF3 (Kapitel 6.2.1), nicht in FF2 — im Deck entsprechend auf Folie 13.

**Belege für die „Bigger-Picture"-Aussagen (Folie 11, Build 2)** — dein To-Do „präzise zuordnen":

| Aussage | Beleg in der Arbeit |
|---|---|
| EBIT-Marge ×1,53/×1,54 in GFC/COVID — operativer Hebel | Kap. 5.2.4 (Verhältnis Peak/Baseline + Deutung Fixkostenstruktur) |
| D/E ×1,37 in Dot-Com — Eigenkapital-Vernichtung im Kurs-Crash | Kap. 5.2.4 (explizit: „mechanisch durch die Eigenkapital-Vernichtung in der Aktienkurs-Korrektur") |
| FCF-Marge nur ×1,11 in GFC — Accrual-Sonderstellung | Kap. 5.2.4 mit Rückverweis auf Kap. 5.1.1 |
| CR überall am schwächsten (1,09–1,24) — träge Bilanzposition | Kap. 5.2.4 mit Rückverweis auf Kap. 4 |

Die Formulierungen „operativer Hebel" und „Krisen-Signatur" sind bewusst Bigger-Picture-Sprache — die Zahlen dahinter sind exakt die aus 5.2.4.

**Diskussionspunkt Synthese-Leiste (Folie 09, Build 3):** Du wolltest klären, ob die Zusatzinfos unten auf der Folie nötig sind. Meine Empfehlung: Die **φ×σ-Karte behalten** — sie ist deine beste Verteidigung gegen die „Median-Split ist willkürlich"-Frage und verdient Sichtbarkeit. Die **Lead-Lag-Karte ist verzichtbar** auf der Folie (Nullergebnis) und könnte in den Sprechtext wandern — dann gewinnt die Folie Luft. Entscheidung liegt bei dir; der Redetext funktioniert in beiden Varianten.

**Noch offen im Deck:** (a) **Fazit-Folie 16** fehlt — Konzept: FF-Karten von Folie 02 kehren per Morph zurück und bekommen ihre Antwortzeilen; (b) optionale **Benchmark-Folie** (mechanische −0,5-Grenze, G2 aus dem Drehbuch) — Redetext dafür liegt oben als Einschub bereit; (c) die vier FF2-Grafik-Platzhalter + FF3-Platzhalter warten auf deine Dark-Renders.

**Zeitreserve:** 19:30 geplant — bei 20:00 Limit bleiben 30 Sekunden Puffer. Kürzungsreihenfolge, falls der Stoppuhr-Durchlauf länger wird: zuerst Folie 10 Build 2 (Tech-Story auf zwei Sätze), dann Folie 06 Zusatzinfo σ-Reihenfolge, zuletzt der Einleitungs-Build. Nie an den Kernzahlen kürzen.
