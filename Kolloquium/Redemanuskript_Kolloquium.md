# Redemanuskript — Masterkolloquium

**Vortrag:** Zeitreihenbasierte Analyse der Dynamik von Finanzkennzahlen börsennotierter Unternehmen
**Ziel-Dauer:** 15:00 (± 1:00) · 13 Folien · ~1 Min./Folie
**Grundlage:** bestehende Foliennotizen, geschärft anhand von `Verteidigungsplan_Kolloquium.md` und `Pruefgutachten_Masterarbeit.md`.
**Zahlen:** exakt aus dem Zahlen-Spickzettel (Verteidigungsplan Abschnitt 7) — unverändert.

> **So liest du dieses Dokument:** Pro Folie steht der Sprechtext zum Verinnerlichen (nicht ablesen) und darunter eine kursive **Regie-Zeile** — sie sagt, *welche* Prüferfrage dieser Abschnitt proaktiv entschärft. Die Regie-Zeilen sprichst du nicht mit.

---

## Folie 1 — Titel · [0:30]

Sehr geehrte Frau Professorin [Name], sehr geehrter Herr Professor [Name], vielen Dank für die Gelegenheit, meine Masterarbeit vorzustellen. Ich habe untersucht, wie sich Finanzkennzahlen börsennotierter US-Unternehmen über die Zeit verhalten — nicht ihre Höhe, sondern ihre Dynamik. In den nächsten 15 Minuten zeige ich, warum sich diese Dynamik systematisch unterscheidet, wie die Kennzahlen zusammenhängen und womit sich die Unterschiede erklären lassen.

*Regie: Ruhiger Einstieg, Blickkontakt. Der letzte Satz ist die Gliederung (FF1–FF3) in einem Atemzug.*

---

## Folie 2 — Einleitung: Leitsatz & Forschungsfragen · [1:00]

Eine Kennzahl wie der ROA ist eine Momentaufnahme — die eigentliche Information steckt in der Bewegung: Kehrt eine Quartalsveränderung im Folgequartal zurück, oder bleibt sie bestehen? Und wie stark schwankt die Kennzahl überhaupt? Diese beiden Dimensionen — Korrekturgeschwindigkeit φ und Veränderungsvolatilität σ — bilden den Gegenstand der Arbeit. Daraus leiten sich drei Forschungsfragen ab: erstens systematische Unterschiede in der Dynamik, zweitens die Interdependenzen zwischen den Kennzahlen und ihr Verhalten über Zeit und Krisen, drittens der Zusammenhang mit strukturellen Unternehmensmerkmalen. Die Zuordnung dieser Dynamiken zu Sektoren ist dabei Teil der ersten Forschungsfrage.

*Regie: Der letzte Satz ist das FF2-Heilungssignal — er nimmt dem Prüfer den Einwand, die Einleitung stelle FF2 anders als Kapitel 5. Wenn dir der Satz zu exponiert ist, kannst du ihn weglassen; er ist bewusst platziert, nicht Füllmaterial.*

---

## Folie 3 — Einleitung: Beitrag der Arbeit · [1:15]

Bevor ich zu den Ergebnissen komme, der eigene Beitrag in drei Punkten. Erstens übertrage ich die Mean-Reversion-Forschung in der Tradition von Fama und French von Jahres- auf Quartalsfrequenz — und von gepoolten auf individuelle Schätzungen, eine pro Unternehmen und Kennzahl. Zweitens behandle ich Korrekturgeschwindigkeit und Volatilität erstmals parallel über sieben Kennzahlen und fasse sie zu einer zweidimensionalen Taxonomie auf Firmenebene zusammen. Und drittens der zentrale neue Befund, auf den die Arbeit hinausläuft: Strukturmerkmale erklären die Volatilität, nicht die Korrekturgeschwindigkeit — φ ist ein eigenständiges, idiosynkratisches Firmenmerkmal. Diesen roten Faden verfolge ich jetzt entlang der drei Forschungsfragen.

*Regie: Wichtigste Reparatur des ganzen Vortrags. Das Gutachten kritisiert, dass die Arbeit ihren Beitrag nie ausformuliert — hier tust du es. Fast wortgleich mit der memorierten „Beitrag in drei Sätzen"-Formel (Prüfungsfrage 11), damit sitzt sie doppelt. Ersetzt die bisher wörtlich von Folie 2 kopierte Notiz.*

---

## Folie 4 — Daten & Stichprobe · [1:00]

Datengrundlage sind Quartalsabschlüsse US-amerikanischer börsennotierter Unternehmen über 25 Jahre — 100 Quartale von 2000 bis 2024, bezogen über die EODHD-API. Aus knapp 5.900 Unternehmen bleibt über eine Filterkette eine finale Stichprobe von 932: der Finanzsektor ausgeschlossen, Doppellistungen und ADRs entfernt, Vollständigkeit über alle 100 Quartale gefordert, Ausreißer winsorisiert. Der Vollständigkeitsfilter erzeugt einen Survivorship Bias — den ich nicht verstecke, sondern beziffere und über alternative Schwellen teste. Am Ende stehen 6.521 Unternehmen-Kennzahl-Kombinationen für sieben Kennzahlen.

*Regie: Survivorship proaktiv nennen (Limitation Nr. 1). „Beziffere und teste" signalisiert Selbstkritik, bevor der Prüfer fragt.*

---

## Folie 5 — Methodik: AR(1) auf ersten Differenzen · [1:15]

Für jede der 6.521 Kombinationen schätze ich ein eigenes AR(1)-Modell — und zwar nicht auf den Niveaus, sondern auf den ersten Differenzen. Dafür drei Gründe: die direkte ökonomische Interpretation der Quartalsveränderung, Stationarität ohne Annahmen über die Niveaus, und Vergleichbarkeit über alle sieben Kennzahlen hinweg. Wichtig für das Verständnis der Ergebnisse: φ misst damit die Autokorrelation der Veränderungen, nicht die Persistenz der Niveaus. Jede Schätzung liefert zwei Parameter — φ, wobei ein negativer Wert Mean-Reversion bedeutet, und σ, die Volatilität der Veränderungen. Über die Firmen aggregiere ich im Mean-Group-Ansatz nach Pesaran und Smith.

*Regie: Der Satz „φ misst die Autokorrelation der Veränderungen, nicht die Persistenz der Niveaus" ist die Vorwegnahme der schärfsten Methodenfrage (weißes Rauschen → φ = −0,5). Betont sprechen — hier legst du die Grundlage für das Spreizungs-Argument auf Folie 13.*

---

## Folie 6 — Methodik: Vier Quadranten im φ–σ-Raum · [1:00]

φ und σ spannen pro Kennzahl einen Raum auf, in dem jedes Unternehmen als ein Punkt liegt. Ein Median-Split in beiden Dimensionen erzeugt vier Dynamiktypen: korrektiv-stabil mit der höchsten Vorhersagbarkeit, korrektiv-volatil, persistent-stabil, und persistent-volatil mit dem höchsten Risiko. Die Logik folgt den Portfolio-Sorts von Fama und French. Und die beiden Achsen tragen unabhängige Information — ihre gemeinsame Variation liegt bei höchstens sechs Prozent.

*Regie: Der Schlusssatz (ρ² ≤ 6 %) entschärft die Frage „Ihr Median-Split ist willkürlich" — die Achsen sind nachweislich unabhängig.*

---

## Folie 7 — FF1: Drei Dynamiktypen nach Kennzahlgruppe · [1:30]

Erste Forschungsfrage, erstes Kernergebnis: drei klar getrennte Schichten. Die Profitabilitätskennzahlen korrigieren am stärksten — φ zwischen −0,43 und −0,46, über 90 Prozent der Schätzungen signifikant. Die Liquidität liegt dazwischen, bei −0,17, und trägt zugleich die höchste Volatilität. Die Kapitalstruktur bleibt nahe null, zwischen −0,04 und −0,09 — bei rund einem Drittel der Unternehmen ohne jede messbare Korrektur. Diese Rangfolge ist robust über vier Modellspezifikationen, vier Stichprobenschwellen und vier Zeitfenster. Die Antwort auf Forschungsfrage eins lautet also: Ja — die Dynamik folgt systematisch den Kennzahlgruppen.

*Regie: Die Robustheit („vier × vier × vier") laut aussprechen — sie ist dein Schutz gegen jeden „ist das Zufall?"-Einwand. Zahlen langsam, sie sitzen im Spickzettel.*

---

## Folie 8 — FF1: Warum? Konstruktion & Korrekturmechanismus · [1:30]

Warum diese Rangfolge? Zwei Mechanismen greifen ineinander. Erstens die Konstruktion der Kennzahlen: Stromgrößen wie die FCF- und die EBIT-Marge korrigieren am stärksten, reine Bestandsgrößen wie die Eigenkapitalquote kaum, und ROA, ROE und Current Ratio liegen als Mischformen dazwischen. Zweitens der ökonomische Korrekturmechanismus: Die Profitabilität wird vom Markt zurückgeholt — Überrenditen ziehen Wettbewerber an; Fama und French messen dafür rund 38 Prozent Rückkehr pro Jahr. Die Kapitalstruktur dagegen kennt keinen solchen Marktmechanismus; sie verändert sich nur, wenn das Management handelt — durch Emission, Rückkauf oder Dividende. Kurz gesagt: Der Markt korrigiert die Profitabilität, das Management die Bilanz.

*Regie: Das ist laut Gutachten die beste Eigenleistung der Arbeit — hier darfst du hörbar überzeugt sein. Der Schlusssatz ist ein Merksatz, mit Pause danach.*

---

## Folie 9 — FF2: Interdependenzen (Matrizen) · [1:15]

Zur zweiten Forschungsfrage, den Interdependenzen. Ich korreliere die geschätzten Parameter paarweise über alle 932 Unternehmen — 21 Kennzahlpaare je Matrix. Bei φ sind nur 9 von 21 Paaren signifikant, und die Kopplung bleibt auf die Profitabilität beschränkt: ROA und ROE bei 0,78. Bei σ dagegen sind es 19 von 21 — die Volatilität koppelt über fast alle Kennzahlen. Daraus der Kernsatz: Schocks treffen die Kennzahlen gemeinsam, korrigiert werden sie kennzahlspezifisch. Rein mechanische Kopplungen — etwa über die DuPont-Identität — weise ich dabei explizit als solche aus, statt sie als ökonomischen Befund zu verkaufen.

*Regie: Der letzte Satz (mechanisch vs. ökonomisch) zeigt methodische Sauberkeit und nimmt der Frage nach Scheinkorrelationen die Spitze.*

---

## Folie 10 — FF2: Dynamik in Krisenphasen · [1:00]

Und über die Zeit? Krisenphasen identifiziere ich datengetrieben über die rollierende Querschnittsvolatilität — 90. Perzentil, mindestens drei Kennzahlen gleichzeitig. Das Verfahren findet ohne jede Vorgabe genau drei Phasen: Dot-Com, Finanzkrise, COVID. In 2009 und 2020 trennt die Quadranten-Klassifikation das Reaktionsverhalten signifikant — der volatile Typ reagiert stärker, bis −0,36. Die Dot-Com-Phase trennt nicht; sie war eine sektorspezifische Tech-Krise. Und ganz wichtig, von mir selbst benannt: Das ist eine In-Sample-Konsistenzprüfung, keine Prognose.

*Regie: In-Sample-Charakter aktiv aussprechen (Limitation Nr. 3). Dass das Verfahren die drei Krisen „ohne Vorgabe" findet, ist ein eleganter Validierungspunkt — betonen.*

---

## Folie 11 — FF3: Struktur erklärt σ, nicht φ · [1:30]

Damit zum Hauptbefund — Forschungsfrage drei. Ich regressiere φ und σ auf fünf Strukturvariablen: Größe, Anlagenintensität, Investitionsintensität, Profitabilitätsniveau und Periodenabgrenzungen. Das Ergebnis ist eine klare Asymmetrie: Die Struktur erklärt im Mittel rund 30 Prozent der Volatilität — bei der FCF-Marge fast die Hälfte —, aber nur rund 5 Prozent der Korrekturgeschwindigkeit. Ökonomisch gelesen heißt das: σ misst Exposition — was ein Unternehmen ist, bestimmt die Größe der Schocks, die es treffen. φ misst Reaktion — wie schnell es korrigiert, ist wettbewerbs- und verhaltensgetrieben und bleibt idiosynkratisch. Genau diese Trennung hält die ganze Arbeit zusammen: Struktur erklärt σ, nicht φ.

*Regie: Die wichtigste Folie des Vortrags und zugleich die Antwort auf Prüfungsfrage 8. Langsamer werden, den Schlusssatz als Kernbotschaft setzen. Wenn du eine Sache perfekt kannst, dann diese.*

---

## Folie 12 — Validierung: Falsifikation & Finanzdienstleister · [1:00]

Zwei Validierungen sichern das ab. Erstens eine falsifikationsorientierte Prüfung: Aus jeder Sektor-Mechanik leite ich eine Vorhersage zur Quadrantenverteilung ab und messe, wie gut sie zutrifft. Drei von vier Clustern bestätigen sich mit 60 bis 66 Prozent; das schwächste — Kommunikation und Energie mit 43 Prozent — benenne ich offen, samt Erklärung. Zweitens der Kontrast zu 451 Finanzdienstleistern: Ihre Current-Ratio-Volatilität liegt beim 29-Fachen der Hauptstichprobe. Der Sektorausschluss vom Anfang ist damit empirisch begründet, nicht bloß Konvention.

*Regie: „Das schwächste benenne ich offen" — Ehrlichkeit als Stärke. Der Bogen zurück zum Sektorausschluss (Folie 4) schließt den Kreis.*

---

## Folie 13 — Limitationen, Ausblick & Fazit · [1:45]

Zu den Grenzen — die ich aktiv nenne. Erstens der Survivorship Bias: Der Vollständigkeitsfilter entfernt 77 Prozent der Unternehmen; getestet habe ich, dass die φ-Mediane bis zur 40-Quartals-Schwelle stabil bleiben — das sind 2.356 Firmen. Zweitens die Differenzen-Konvention: φ misst Veränderungs-Autokorrelation, nicht Niveau-Persistenz. Entscheidend ist deshalb nicht der absolute Wert, sondern die Spreizung zwischen den Kennzahlen — von −0,43 bis −0,46 bei der Profitabilität bis nahe null bei der Kapitalstruktur. Genau diese Spreizung ist ökonomisch, nicht mechanisch. Drittens der In-Sample-Charakter der Krisentests, und viertens der Geltungsbereich: etablierte US-Unternehmen auf Quartalsfrequenz — Effekte unterhalb eines Quartals und andere Märkte bleiben offen. Dort setzt der Ausblick an: ein Out-of-Sample-Test der Quadranten, Lead-Lag auf den AR-Residuen, höhere Datenfrequenz und Märkte jenseits der USA.

Zusammengefasst: Die Arbeit vermisst die Dynamik von sieben Finanzkennzahlen in einem φ-σ-Raum, findet drei robuste Dynamiktypen und zeigt als zentrales Ergebnis, dass die Struktur eines Unternehmens seine Volatilität erklärt — seine Korrekturgeschwindigkeit dagegen bleibt idiosynkratisch. Vielen Dank für Ihre Aufmerksamkeit — ich freue mich auf Ihre Fragen.

*Regie: Zwei Bewegungen. (1) Limitationen + Ausblick — das eingebettete Spreizungs-Argument entschärft die weiße-Rauschen-Frage vorab. (2) Schluss-Kernbotschaft + Dank. Nach „Ihre Fragen" bewusst schweigen und den Blick heben. Das ist dein Landepunkt — ihn auswendig können.*

---

## Timing-Übersicht

| Folie | Thema | Zeit |
|---|---|---|
| 1 | Titel | 0:30 |
| 2 | Leitsatz & Forschungsfragen | 1:00 |
| 3 | Beitrag der Arbeit | 1:15 |
| 4 | Daten & Stichprobe | 1:00 |
| 5 | Methodik AR(1) | 1:15 |
| 6 | Vier Quadranten | 1:00 |
| 7 | FF1 — Drei Dynamiktypen | 1:30 |
| 8 | FF1 — Warum? | 1:30 |
| 9 | FF2 — Matrizen | 1:15 |
| 10 | FF2 — Krisen | 1:00 |
| 11 | FF3 — Struktur erklärt σ, nicht φ | 1:30 |
| 12 | Validierung | 1:00 |
| 13 | Limitationen, Ausblick & Fazit | 1:45 |
| | **Summe** | **~15:30** |

**Wenn es straffer werden muss (Ziel 15:00 oder 12:00):** zuerst Folie 6 auf 0:45 und Folie 9 auf 1:00 kürzen; bei 12 Minuten Folie 6 rein visuell zeigen (ohne Kommentar zur Portfolio-Sort-Logik) und Folie 10 auf 0:45.
**Wenn 20 Minuten bestätigt werden:** je 30 Sekunden mehr auf Folie 8 (zweites Beispiel) und Folie 11 (DuPont-Anbindung der Markt-vs.-Management-Logik).

## Was gegenüber deinen bisherigen Notizen geändert wurde

1. **Folie 3** komplett neu — statt Wortduplikat von Folie 2 jetzt die drei Beiträge (= Reparatur der größten inhaltlichen Gutachten-Kritik).
2. **Folie 13** um Ausblick, Schluss-Kernbotschaft und Dank/Übergang erweitert; Spreizungs-Argument eingebaut.
3. **Folie 2** um das FF2-Heilungssignal ergänzt (Sektor-Zuordnung = Teil von FF1).
4. **Folien 5, 6, 9, 10, 12** mit je einem geschärften Regie-Satz, der die zugehörige Prüfungsfrage vorab entschärft.
5. Durchgängig: Verben variiert, Übergänge zwischen den Forschungsfragen ergänzt, Terminologie an die Foliensprache angeglichen (Korrekturgeschwindigkeit / Volatilität / Dynamiktypen).

*Alle Zahlen unverändert aus dem Zahlen-Spickzettel. Neu ergänzt wurden ausschließlich Formulierungen, keine Werte.*
