# Prüfgutachten zur Masterarbeit

**Thema:** Zeitreihenbasierte Analyse der Dynamik von Finanzkennzahlen börsennotierter US-Unternehmen — AR(1) auf ersten Differenzen, 932 Unternehmen, Q1/2000 bis Q4/2024
**Verfasser:** Tobias Mourier · TH Wildau · Abgabedatum laut Erklärung: 21.05.2026
**Perspektive dieses Gutachtens:** simulierte Prüferrolle. Geprüft werden Forschungsleistung und Erkenntnisgewinn, Methodik, Struktur und Argumentation, Formalia, sprachliche Konsistenz (inklusive Hinweisen auf heterogene Textentstehung) sowie die voraussichtlichen Angriffspunkte im Kolloquium. Grundlage ist ausschließlich das vorgelegte PDF. Code, Rohdaten und der im Text erwähnte Anhang lagen nicht vor — das ist selbst ein Prüfungsbefund, dazu unten mehr.

---

## 1. Gesamteinordnung: Was wurde geforscht, was wurde gefunden?

### 1.1 Forschungsgegenstand und Design

Die Arbeit untersucht nicht die Niveaus, sondern die *Dynamik* von sieben Finanzkennzahlen (ROA, ROE, EBIT-Marge, FCF-Marge, Current Ratio, Debt/Equity, Eigenkapitalquote). Für jede der rund 6.500 Unternehmen-Kennzahl-Kombinationen wird ein individuelles AR(1)-Modell auf ersten Differenzen geschätzt (Mean-Group-Ansatz nach Pesaran/Smith). Daraus entstehen zwei Parameter pro Kombination: der Mean-Reversion-Koeffizient φ und die Veränderungsvolatilität σ(ΔY). Ein Median-Split in beiden Dimensionen erzeugt eine Vier-Quadranten-Taxonomie (Korrektiv/Persistent × Stabil/Volatil), die anschließend auf Sektoren, Krisenphasen und strukturelle Unternehmensmerkmale bezogen wird. Drei Forschungsfragen strukturieren die Arbeit: systematische Dynamikunterschiede (FF1), Interdependenzen und zeitliches Verhalten (FF2), Zusammenhang mit Unternehmensmerkmalen (FF3).

Es handelt sich um eine deskriptiv-taxonomische, empirisch getriebene Arbeit. Sie testet keine kausale Hypothese, sondern vermisst ein Feld und ordnet es. Das ist für eine Masterarbeit ein legitimes und ehrliches Design — vorausgesetzt, die Vermessung ist methodisch sauber und die Einordnung geht über reine Datenbeschreibung hinaus. Beides ist überwiegend, aber nicht durchgängig der Fall.

### 1.2 Kernbefunde

Die Arbeit liefert vier substanzielle, intern konsistente Befunde:

1. **Drei Dynamiktypen entlang der Kennzahlgruppen.** Profitabilitätskennzahlen revertieren stark (φ-Median ≈ −0,43 bis −0,46), Liquidität moderat (−0,17), Kapitalstruktur kaum (−0,04 bis −0,09). Diese Hierarchie ist robust über vier Modellspezifikationen, vier Stichprobenschwellen und vier Zeitfenster.
2. **Korrekturgeschwindigkeit ist ein Firmenmerkmal, aber nur innerhalb der Profitabilität.** Die φ-Werte von ROA, ROE und EBIT-Marge korrelieren stark (ρ bis 0,78), über Dynamiktypen hinweg jedoch kaum. Die σ-Matrix ist dagegen dicht gekoppelt: Schocks treffen Kennzahlen gemeinsam, korrigiert werden sie kennzahlspezifisch. Die FCF-Marge nimmt eine begründbare Sonderrolle ein (Accrual-Mechanik nach Sloan/Dechow).
3. **Strukturmerkmale erklären σ, nicht φ.** Multivariat erklären fünf Strukturvariablen im Mittel ~30 % der Volatilitätsvariation, aber nur ~5 % der Mean-Reversion-Variation. Diese Asymmetrie ist das prägnanteste und am besten verteidigbare Einzelergebnis der Arbeit.
4. **Validierungen tragen.** Die datengetriebene Krisenidentifikation trifft Dot-Com, Finanzkrise und COVID; die Quadranten trennen das Krisenverhalten in zwei von drei Phasen signifikant; der Finanzdienstleister-Kontrast (29-fache Current-Ratio-Volatilität) rechtfertigt den Sektorausschluss empirisch statt nur per Konvention.

Bemerkenswert positiv: Über gut 90 Seiten hinweg sind die zentralen Zahlen (z. B. 6.521 Kombinationen, 11 % positive φ-Schätzungen, die Kennzahl-Mediane) in sich konsistent, wo immer sie wieder auftauchen. Das spricht für eine gepflegte Datenbasis und gegen zusammenkopierte Ergebnisse.

### 1.3 Wissenschaftlicher Beitrag — und seine ungenutzte Verteidigung

Der Beitrag liegt in der *Kombination*: individuelle AR(1)-Schätzung auf Quartalsfrequenz × sieben Kennzahlen parallel × Quadranten-Taxonomie × Strukturvariablen-Erklärung. Einzeln ist nichts davon neu (Fama/French 2000 für Profitabilitäts-Mean-Reversion, Pesaran/Smith für Mean-Group, Fama/French-Sorts für die Klassifikationslogik), die Zusammenführung auf Firmenebene mit explizitem φ-σ-Raum ist aber eine eigenständige Leistung.

Das Problem: **Die Arbeit formuliert ihren eigenen Beitrag nie aus.** Kapitel 2 kündigt einen Abschnitt zur Forschungstradition und einen Abschnitt zum Beitrag der Arbeit an — beide existieren nicht (stattdessen stehen dort zwei „Fehler! Verweisquelle konnte nicht gefunden werden."). Ein Prüfer, der den Erkenntnisgewinn bewerten soll, muss ihn sich aus Kapitel 6 und 7 selbst zusammensuchen. Das kostet in der Bewertung der Kategorie „Einordnung in den Forschungsstand" fast zwangsläufig Punkte, obwohl der Beitrag faktisch vorhanden ist.

---

## 2. Kapitelweise Prüfung

### 2.0 Verzeichnisse und Gesamtaufbau

Inhalts-, Abbildungs- und Tabellenverzeichnis sind vorhanden und vollständig. Es fehlen: ein Abkürzungs- und Symbolverzeichnis (φ, σ, IQR, K-V/K-S/P-V/P-S, GICS, REIT, CapEx werden intensiv genutzt) und der Anhang, auf den Kapitel 5.2.2 explizit verweist („Übersichtsplots pro Kennzahlgruppe finden sich im Anhang") — im Dokument existiert kein Anhang. Die Gewichtung ist stark empirielastig: ~5 Seiten Theorie gegenüber ~70 Seiten Ergebnissen. Für eine empirische Arbeit vertretbar, aber das Theoriekapitel ist auch qualitativ das schwächste (siehe 2.2).

### 2.1 Kapitel 1 — Einleitung

**Inhalt und Funktion:** Motivation über Business Analytics, Hinführung über die Walmart-EBIT-Zeitreihe, Zielformulierung, drei Forschungsfragen, Gang der Untersuchung. Die Forschungsfragen sind klar und operationalisierbar — das ist die wichtigste Funktion der Einleitung, und sie wird erfüllt.

**Schwächen aus Prüfersicht:**

- Der Einstieg über Taylorismus und „Scientific Management" ist generisch, unbelegt und trägt nichts zur konkreten Fragestellung bei. Ein strenger Prüfer streicht die erste halbe Seite als Füllmaterial an.
- Abbildung 1 beschriftet das EBIT von Walmart mit „Milliarden €" — ein US-Unternehmen mit Quartalsdaten aus einer US-API wird in Euro ausgewiesen. Mit hoher Wahrscheinlichkeit ein Einheitenfehler (USD). Klein, aber auf Seite 1 prominent platziert.
- **FF2 wird hier anders formuliert als später beantwortet.** In der Einleitung lautet FF2: „Lassen sich diese Dynamiken bestimmten Kennzahlgruppen oder Sektoren zuordnen?" — das beantwortet faktisch Kapitel 4 (Analyse nach Kennzahl und Sektor). Kapitel 5 eröffnet dagegen mit einer anderen FF2: „Welche Interdependenzen bestehen zwischen Finanzkennzahlen und inwieweit unterscheiden sich diese zwischen Unternehmen?" Die Arbeit beantwortet damit still eine andere Frage als angekündigt. Das ist kein kosmetisches Problem, sondern ein Konsistenzbruch im Forschungsdesign, den ein Prüfer fast sicher anspricht.
- Die Entscheidung für den Median als zentrale Größe wird in einem Satz gesetzt, nicht begründet (Robustheit gegen Ausreißer/Schiefe wäre die naheliegende Begründung — sie fehlt hier und wird erst implizit in 3.4.3 nachgeliefert).
- Es fehlt eine Relevanz-Adressierung: Für wen sind die Ergebnisse nützlich (Analysten, Controlling, Kreditvergabe, Prognosemodelle)? Die Arbeit bleibt das bis Kapitel 7 schuldig.

**Zwischenfazit Kap. 1:** funktional, aber unter dem Niveau des empirischen Teils. Note der Einzelteilleistung: befriedigend.

### 2.2 Kapitel 2 — Stand der Forschung

**Inhalt:** 2.1 definiert die sieben Kennzahlen sauber und einheitlich mit Formelbezug zur Datenbasis (gute Entscheidung, die englischen Feldnamen beizubehalten und das zu begründen). 2.2 führt das AR(1)-Modell, OLS-Schätzung, R² und den Signifikanztest ein. 2.3 begründet die Differenzenbildung über die Stationaritätsanforderung.

**Schwächen — hier liegt die strukturell schwerste Stelle der Arbeit:**

- Der Kapiteleinstieg kündigt vier Abschnitte an; für die Abschnitte „Forschungstradition" und „Beitrag der Arbeit" stehen zwei tote Querverweise („Fehler! Verweisquelle konnte nicht gefunden werden.") — die Abschnitte existieren nicht. Das angekündigte Fundament der Arbeit fehlt ersatzlos.
- Es gibt **keinen echten Literaturüberblick** zur empirischen Mean-Reversion-Forschung. Fama/French (2000) — die zentrale Referenzarbeit — wird erst in Kapitel 4.3.1 inhaltlich eingeführt. Sloan (1996), Dechow (1994), Pesaran/Yang (2024) tauchen verstreut in Methodik und Ergebnissen auf. Ein Prüfer erwartet diese Verortung *vor* der Methodik, inklusive einer expliziten Forschungslücke.
- Die AR-Grundlagen stützen sich tragend auf ein Vorlesungsskript („Stollhoff, WS 2023/2024", Moodle-Link). Das ist zitierfähig, aber für eine Masterarbeit als Hauptquelle der Modelltheorie dünn — Hamilton (1994) steht im Literaturverzeichnis und hätte diese Rolle übernehmen müssen.
- Kapitel 2.3 endet mitten im Satz: „Aus diesem Grund wird in dieser Arbeit die erste Differenz der Zeitreihe als Inputvariable für das AR(1) Modell" — das Verb fehlt. Ein abgebrochener Satz im Theoriekapitel ist ein deutliches Signal fehlender Endkontrolle.
- Kleinere Punkte: Die DuPont-Zerlegung wird eingeführt mit Verweis auf „Kapitel 4.3.2" — korrekt, aber die Quelle „DuPont schlägt vor" ist unbelegt; die Sekundärzitierung „Charifzadeh und Taschner 2017, zitiert nach Steglich 2024" ist formal zulässig, bei verfügbarer Primärquelle aber vermeidbar.

**Zwischenfazit Kap. 2:** Die Kennzahldefinitionen sind solide, der Rest ist das schwächste Kapitel der Arbeit — unfertig im Wortsinn. Note der Einzelteilleistung: ausreichend bis befriedigend.

### 2.3 Kapitel 3 — Methodik

**Stärken (und davon gibt es hier viele):**

- Die Filterkette (Tabelle 1) ist vorbildlich transparent: jeder Schritt mit Vorher/Entfernt/Nachher und Begründung. Von 5.871 auf 932 Unternehmen nachvollziehbar dokumentiert.
- Der Survivorship Bias wird nicht versteckt, sondern beziffert (77 % Ausschluss) und in 3.4.2 mit vier alternativen Schwellen getestet — die φ-Mediane bewegen sich um maximal 1–2 Prozentpunkte. Das ist genau die Sorte Selbstkritik, die Prüfer sehen wollen.
- Das Ausreißerverfahren (Multi-Window, Mehrfachbedingung, dokumentierte manuelle Prüfliste) ist detailliert beschrieben; die Winsorisierung wird mit Adams et al. (2019) sogar gegen die eigene Methode kritisch reflektiert und in ihrer Rolle korrekt herabgestuft.
- Die Modellwahl wird gegen vier Alternativen (AR(2), Niveaus, saisonale Differenzen, Doppeldifferenzen) getestet, die Mean-Group-Logik mit Pesaran/Smith (1995) und Pesaran/Yang (2024) korrekt verortet. Das Robustheitsprogramm in vier Dimensionen (3.4.1–3.4.4) liegt über dem üblichen Masterniveau.
- Die statistische Werkzeugwahl ist durchdacht: nichtparametrische Tests (Spearman, Mann-Whitney, Kruskal-Wallis), Bonferroni-Korrekturen, und — wichtig — die explizite Priorisierung von Effektstärken über p-Werte bei N = 932.

**Schwächen:**

- **Gleichung (12) — die zentrale Modellgleichung der gesamten Arbeit — ist fehlerhaft gesetzt:** „ΔY = c + φ + ⋯ ΔY(t−1) + ε". Das Pluszeichen nach φ und das Fragment „+ ⋯" sind falsch; korrekt wäre c + φ·ΔY(t−1) + ε. Inhaltlich weiß die Arbeit, was gemeint ist (Gleichung 10 ist korrekt), aber ein Formelfehler im Hauptmodell ist für Prüfer ein gefundenes Fressen.
- 3.2.2 enthält einen weiteren Satzabbruch: „Das AR(1)-Modell und die Interpretation des Koeffizienten φ wurden in Kapitel 2.2." (Verb fehlt). 3.3 verweist auf „Kapitel 3.2.1" statt 3.3.1. Die Überschrift 3.4 lautet „Rohbustheitsanalysen" (Tippfehler, auch im Inhaltsverzeichnis).
- **Keine formalen Stationaritätstests.** Die Arbeit argumentiert in 2.3 ausführlich über Stationarität, berichtet aber keinen einzigen ADF-/KPSS-Test. Die Differenzenbildung wird pauschal gesetzt. Das ist verteidigbar (einheitliche Transformation als bewusster Vergleichbarkeits-Kompromiss, in 3.2 sogar explizit so benannt), aber die Testlücke wird im Kolloquium kommen.
- **Die zentrale methodische Flanke wird nicht adressiert: der Differenzen-Benchmark.** Wer eine Zeitreihe differenziert, deren Niveaus näherungsweise unkorreliert sind (oder stark von Messrauschen geprägt), erhält *mechanisch* ein φ nahe −0,5 — ohne jede ökonomische Mean-Reversion. Die beobachteten Profitabilitäts-φ von −0,43 bis −0,46 liegen genau in dieser Zone, und das AR(2)-Ergebnis (−0,56) ist mit einer durch Überdifferenzierung induzierten MA-Struktur konsistent. Die Arbeit formuliert zwar vorsichtig („messen die Autokorrelationsstruktur der Quartalsveränderungen, nicht wirkliche Persistenz"), rechnet den Benchmark aber nie vor. Wichtig: Die Arbeit *hätte* hier ein starkes Gegenargument — wäre φ ≈ −0,5 reine Mechanik, müssten alle sieben Kennzahlen dort liegen; die Kapitalstruktur liegt bei ≈ 0. Dieses Argument steht implizit in den Daten, wird aber nirgends explizit geführt. (Für das Kolloquium: unbedingt aktiv vortragen können, siehe Abschnitt 6.)
- Querschnittsabhängigkeit (gemeinsame Schocks über Firmen, z. B. Krisen) bleibt unbehandelt, obwohl Kapitel 5 sie mit der dichten σ-Korrelationsmatrix selbst nachweist. Individuelle OLS-Schätzungen sind davon im Punktschätzer wenig betroffen, die aggregierten Signifikanzraten („92 % signifikant") können aber überzeichnet sein.

**Zwischenfazit Kap. 3:** inhaltlich-konzeptionell gut bis sehr gut, handwerklich (Formeln, Verweise, Sätze) mangelhaft redigiert. Note der Einzelteilleistung: gut, mit formalem Abzug.

### 2.4 Kapitel 4 — Ergebnisse FF1: Dynamikmuster

**Stärken:**

- Die Befundarchitektur ist stringent: erst der Gesamtraum (Abb. 4–6), dann die drei Gruppen einzeln (4.1.2–4.1.4) mit jeweils vollständiger Statistik-Tabelle (Median, IQR, R², Signifikanzraten roh und Bonferroni-korrigiert, Anteil φ < 0). Diese Tabellen sind das Rückgrat der Arbeit und halten einer Prüfung stand.
- Besonders stark: die Detektivarbeit an den positiven φ-Werten. Die Arbeit zeigt für Profitabilität, Liquidität und Kapitalstruktur jeweils separat, dass positive φ mit R² nahe null und null Bonferroni-Signifikanz einhergehen — also Modellartefakte statt eigenständiger Dynamik sind. Das ist eigenständiges, kritisches Arbeiten mit den eigenen Ergebnissen.
- Kapitel 4.3 ist die beste Eigenleistung der Arbeit: die Strom-vs.-Bestandsgrößen-Mechanik (4.3.2, inkl. DuPont-Zerlegung zur Erklärung der ROA/ROE-Differenz) und die Markt-vs.-Management-Logik (4.3.1, sauber an Pecking-Order-, Market-Timing- und Trade-off-Theorie angebunden) erklären die gefundene φ-Hierarchie schlüssig und theoriegestützt. Hier zeigt die Arbeit Verständnis statt nur Beschreibung.

**Schwächen:**

- Tabelle 7 (Liquidität) trägt die Spaltenüberschrift „FCF-Marge", enthält aber die Current-Ratio-Werte. Ein Copy-Paste-Fehler an einer zentralen Ergebnistabelle.
- In 4.1.3 ist der Abbildungstitel in den Fließtext gerutscht („In Abbildung 8: Liquidität – Quadranten-Verteilung pro Kennzahl liegt der φ-Median…").
- Kapitel 4.2.2 (Quadrantenverteilung pro Sektor) ist mit ~12 Seiten das längste Unterkapitel und teilweise redundant zur Heatmap selbst; die Branchenerklärungen sind plausibel, aber überwiegend ad hoc und unbelegt (z. B. Gesundheitssektor: „Pharmaunternehmen und zyklischere Medizintechnik gleichen sich beim Mitteln aus" — eine testbare Hypothese, die nicht getestet wird; erst 6.2.2 holt das teilweise nach). Genau hier häufen sich außerdem die Grammatikfehler („die Sektor", „in jeder Sektor", „der einzige Branche") — dazu Abschnitt 4 dieses Gutachtens.
- Direkt vor Abbildung 14 steht erneut ein toter Verweis („Fehler! Verweisquelle konnte nicht gefunden werden. stellt dies in einer Heatmap dar").
- Die Einleitung zu 4.3 kündigt fünf Interpretations-Unterkapitel an (4.3.1 bis 4.3.5, inkl. „4.3.3 zeigt, was σ gegenüber φ über das Geschäftsmodell aussagt" und „4.3.5 fasst zusammen") — es existieren nur drei (4.3.1–4.3.3). Zusätzlich ist die Ankündigung selbst verstümmelt („4.1.14.3.1 erklärt…"). Zwei angekündigte Analysen fehlen ersatzlos.
- Kleinigkeiten: „Dept/Equity" statt „Debt/Equity" (mehrfach), Klammerfehler („belegt mit (φ ≈ −0,50 den vordersten Platz"), uneinheitliche Schreibweisen („zweit stabilste", „Volatilitätsstärkste").

**Zwischenfazit Kap. 4:** Das empirische Herzstück trägt. FF1 wird vollständig und differenziert beantwortet, die Interpretation in 4.3 hebt die Arbeit über reine Deskription. Abzüge für Redundanz, fehlende angekündigte Abschnitte und Schludrigkeiten. Note der Einzelteilleistung: gut.

### 2.5 Kapitel 5 — Ergebnisse FF2: Interdependenzen und zeitliche Dynamik

**Stärken:**

- Die φ- und σ-Korrelationsmatrizen sind methodisch sauber (Spearman, Bonferroni-Schwelle α/21 ausgewiesen) und werden klug gelesen: mechanische Kopplungen (ROE×D/E über DuPont, EBIT×FCF über den gemeinsamen Umsatznenner) werden explizit als nicht-ökonomisch markiert statt als Befund verkauft. Das ist ein Qualitätsmerkmal.
- Die Lead-Lag-Analyse liefert ein Nullergebnis — und die Arbeit berichtet es als solches, inklusive zweier konkreter Gründe für die begrenzte Aussagekraft (mechanische Überlagerung durch Mean-Reversion; Quartalsfrequenz zu grob) und des korrekten Lösungswegs (Residuen-Korrelation). Ehrliche Nullergebnisse mit Methodenreflexion sind selten und positiv zu würdigen.
- Die Peak-Window-Identifikation ist datengetrieben definiert (90. Perzentil, ≥3 Kennzahlen) und trifft exakt Dot-Com, GFC und COVID — eine elegante interne Validierung.
- 5.2.3 enthält die wichtigste Selbstrelativierung der Arbeit: die Quadranten-Trennung in Krisen ist eine In-Sample-Konsistenzprüfung, keine Out-of-Sample-Vorhersage. Dass die Arbeit das selbst sagt, bevor es der Prüfer tut, ist taktisch und wissenschaftlich genau richtig.

**Schwächen:**

- **Der Bruch in der Forschungsfrage** (siehe 2.1 dieses Gutachtens): Kapitel 5 beantwortet eine anders formulierte FF2 als die Einleitung stellt. Die Zuordnungsfrage der Einleitung wurde bereits in Kapitel 4.2 miterledigt; sauber wäre gewesen, das explizit zu machen und die FF konsistent zu halten.
- Im Kapiteleinstieg steht ein kaputter Querverweis: „Kapitel 0 betrachtet wie sich die Streuung…". Auf S. 65 erneut: „Vergleiche in 5.2.3 bis Fehler! Verweisquelle…".
- 5.2.2 (Drift-Analysen pro Sektor, ~8 Seiten) fällt aus dem Rahmen: Verweis auf einen nicht vorhandenen Anhang; plötzlich englische Sektornamen („Real Estate", „Healthcare", „Communication Services", „Consumer Cyclical") parallel zu den sonst deutschen Bezeichnungen; eine erkennbar andere Textur (dazu Abschnitt 4). Inhaltlich ist der Abschnitt stark zahlengetrieben-narrativ und bewegt sich an der Grenze zur Datenreportage; der analytische Mehrwert pro Seite ist geringer als in Kapitel 4. Die Schlussbetrachtung (Krisen-Marker, AR(1)-Eignung über R² der Trend-Regression) holt das teilweise zurück.
- Einzelbefund mit Erklärungsbedarf: Bei Immobilien fällt die D/E-Niveau-Linie (Trend −0,25), der c-Median ist aber positiv (+0,0009). Die Arbeit erklärt das in einem Halbsatz („weil der c-Median über die Firmen anders verteilt ist als der Aggregat-Trend") — korrekt, aber so knapp, dass im Kolloquium eine Nachfrage wahrscheinlich ist (Median-vs.-Aggregat-Logik, Schiefe der Firmenverteilung).

**Zwischenfazit Kap. 5:** methodisch diszipliniert mit vorbildlicher Selbstkritik, strukturell aber durch den FF2-Bruch und den Stil-/Formatwechsel in 5.2.2 belastet. Note der Einzelteilleistung: gut bis befriedigend.

### 2.6 Kapitel 6 — Ergebnisse FF3: Dynamiktypen und Unternehmensmerkmale

**Stärken:**

- Die Asymmetrie-These (Strukturvariablen erklären ~30 % von σ, ~5 % von φ; 31 von 49 σ-Tests vs. 10 von 49 φ-Tests Bonferroni-signifikant) ist klar herausgearbeitet, zieht sich konsistent durch alle Unterkapitel und wird in 6.3 prägnant zur Antwort auf FF3 verdichtet. Das ist die reifste Ergebnisformulierung der Arbeit.
- Die Cluster-Falsifikation (6.2.2) ist methodisch erfreulich: Aus den ökonomischen Mechaniken von 4.3.3 werden testbare Vorhersagen abgeleitet, Konformitätsquoten gemessen, und das schwächste Cluster (Komm./Energie, 43 %) wird offen als schlecht bestätigt benannt — inklusive Erklärung, *warum* (Investitionszyklen persistieren den Cashflow länger als ein Quartal). Falsifikationslogik statt Bestätigungssuche.
- Die sechs Beispielunternehmen (MGEE, Tractor Supply, McDonald's, Applied Materials, Walmart, Texas Instruments) übersetzen die abstrakte Taxonomie in lesbare Zeitreihen; das MGEE-vs.-Walmart-Paar (gleicher Quadrant, verschiedene ökonomische Mechanik) und TXN als Beleg, dass das Modell Persistenz abbilden *kann*, sind didaktisch und argumentativ wertvoll.
- Der Finanzdienstleister-Kontrast (6.2.3, n = 451) verwandelt eine Ausschlusskonvention in einen empirischen Robustheitsbefund. Gute Idee, gut umgesetzt.

**Schwächen:**

- Erneut tote Querverweise an tragenden Stellen: im Kapiteleinstieg („Kapitel Fehler! … fasst die Erklärungsbeiträge … zusammen", gemeint ist 6.3), in 6.1 („Kapitel Fehler! Verweisquelle …" für 6.1.1) und zweifach in 6.1.2.
- **Eine in der Methodik angekündigte Analyse fehlt:** 3.5.3 kündigt an, die Quadrantenklassifikation als kategoriale Kontrollvariable in die multivariaten Regressionen aufzunehmen, „um die Restinformation der Klassifikation jenseits der strukturellen Merkmale zu prüfen". Auch der Kapiteleinstieg von 6 verspricht genau dieses Ergebnis. In 6.3 wird es nicht berichtet. Da genau diese Restinformation den Mehrwert der eigenen Taxonomie beziffern würde, ist das eine empfindliche Lücke — der Prüfer wird fragen: „Was kam dabei heraus?"
- Die multivariaten OLS-Regressionen (6.3) kommen ohne jede Diagnostik: Die drei Größenmaße (Marktkapitalisierung, Bilanzsumme, Mitarbeiter) sind hochkorreliert — Multikollinearität (VIF) wird nicht geprüft oder zumindest nicht berichtet; ebenso fehlen Angaben zu Koeffizienten/Vorzeichen (nur R² wird gezeigt).
- 6.1.4 (Accruals nach Sloan): Die Vorzeichenkonvention und die Interpretation „hohe Periodenabgrenzungen = geglättete Buchgewinne" wird gesetzt, aber nicht gegen die alternative Lesart (hohe Accruals = niedrige Ertragsqualität = eher volatilere Folgegewinne, Sloans ursprüngliche Pointe) abgegrenzt. Angreifbar im Kolloquium.

**Zwischenfazit Kap. 6:** das analytisch reifste Ergebniskapitel mit einem klaren Hauptbefund — geschmälert durch die fehlende angekündigte Quadranten-Restinformations-Analyse und fehlende Regressionsdiagnostik. Note der Einzelteilleistung: gut.

### 2.7 Kapitel 7 — Zusammenfassung und Ausblick

- Die Zusammenfassung der FF1 und FF2 ist korrekt und kompakt. Auffällig: Die FF3-Antwort wird *weicher* formuliert als in Kapitel 6 („dürften … häufiger stabilere Muster aufweisen", „können volatilere Verläufe zeigen") — Kapitel 6 hat quantitativ präzise geliefert (30 % vs. 5 %), Kapitel 7 verschenkt diese Präzision. Das Aussageniveau der Arbeit sinkt ausgerechnet auf der letzten Seite.
- **Es gibt keinen Ausblick**, obwohl der Kapiteltitel ihn verspricht und die Einleitung ihn ankündigt. Keine Limitationen-Synthese (Survivorship Bias, US-only, Quartalsfrequenz, In-Sample-Charakter wären zu bündeln gewesen), keine Future-Research-Linien (naheliegend: Out-of-Sample-Test der Quadranten, Residuen-Lead-Lag, Monatsdaten, Nicht-US-Märkte, Prognosenutzen), keine Praxisimplikationen. Für ein Schlusskapitel ist das zu wenig — hier verliert die Arbeit auf der Zielgeraden.

**Zwischenfazit Kap. 7:** ausreichend bis befriedigend; die schwächste Stelle nach Kapitel 2.

### 2.8 Quellenverzeichnis und Zitierpraxis

- Umfang: ~20 Quellen. Für eine Masterarbeit dieses Umfangs knapp, aber die Kernliteratur (Fama/French 1993/2000/2015, Sloan, Dechow, Myers, Frank/Goyal, Bates et al., Pesaran/Smith, Pesaran/Yang, Hamilton) ist vorhanden und wird inhaltlich korrekt eingesetzt. Aktuelle Literatur nach 2015 ist mit Pesaran/Yang (2024) fast allein.
- Konkrete Mängel: Baker/Wurgler (2002) ohne Aufsatztitel und mit falsch geschriebenen Vornamen („Malcom", „Jefferey"); Fama/French „Forecasting Profitability and Earnings" doppelt gelistet (1999 und 2000, identischer Titel); uneinheitliche Formate (Verlagsadresse mit Straße bei Hamilton, „CHICAGO JOURNALS" als Quelle bei Comin/Philippon); im Fließtext „Nissim und Penman 2001; Christie 1982" zitiert (5.1.2), beide fehlen im Verzeichnis — ein klassischer Abgleichfehler, den Prüfer systematisch suchen.
- Das Vorlesungsskript als tragende Theoriequelle: siehe 2.2.

---

## 3. Konsolidierte formale Mängelliste

Die folgenden Punkte sind im Dokument verifizierbar und in einer Prüfung praktisch sicher relevant. Sortiert nach Schwere.

**Kategorie A — strukturwirksam (kosten in fast jedem Bewertungsraster Punkte):**

1. Mindestens acht tote Querverweise „Fehler! Verweisquelle konnte nicht gefunden werden." (Kap.-2-Einstieg 2×, vor Abb. 14, S. 65 in 5.2.1, Kap.-6-Einstieg, 6.1, 6.1.2 2×) plus der Verweis „Kapitel 0" im Kap.-5-Einstieg. Befund: Die Word-Felder wurden vor dem PDF-Export nicht aktualisiert/geprüft.
2. Angekündigte, aber nicht existierende Abschnitte: Forschungstradition und Beitrag der Arbeit (Kap. 2), 4.3.4 und 4.3.5 (Kap.-4.3-Einstieg), Quadranten-Restinformations-Analyse (angekündigt in 3.5.3 und Kap.-6-Einstieg), Anhang (referenziert in 5.2.2), Ausblick (Kapiteltitel 7).
3. Inkonsistente Formulierung der FF2 zwischen Einleitung und Kapitel 5.
4. Gleichung (12) fehlerhaft gesetzt (Hauptmodell).
5. Zwei Satzabbrüche an tragenden Stellen (Ende 2.3; 3.2.2).
6. Tabelle 7 mit falscher Spaltenüberschrift („FCF-Marge" statt „Current Ratio").
7. Im Text zitierte, im Verzeichnis fehlende Quellen (Nissim/Penman 2001; Christie 1982).

**Kategorie B — auffällig, aber lokal:**

8. Durchgängige Genusfehler bei „Sektor" („die Sektor", „in jeder Sektor", „keine andere Sektor", „die nächstgrößte Sektor") und einmal umgekehrt („der einzige Branche", S. 45). Das Muster deutet auf ein spätes globales Ersetzen von „Branche" durch „Sektor" ohne Nachredaktion — als Erklärung im Kolloquium sogar verwendbar, als Befund trotzdem ein Sprachmangel mit hoher Frequenz (zweistellige Trefferzahl).
9. Überschrift „Rohbustheitsanalysen" (3.4, auch im Inhaltsverzeichnis); „Bonferoni" in den Beschriftungen von Abb. 16/17; „Dept/Equity" mehrfach.
10. Abbildung 1: Walmart-EBIT in „Milliarden €" statt USD.
11. Abbildungstitel in Fließtext gerutscht (4.1.3); Textfragment „nur Quadrantendie EBIT-Marge in K-V" (4.2.2, Grundstoffe); verschmolzene Verweise („4.1.14.3.1 erklärt", 4.3); Klammerfehler („mit (φ ≈ −0,50 den vordersten Platz", 4.2.1).
12. Terminologiewechsel in 5.2.2 zu englischen Sektornamen (Real Estate, Healthcare, Communication Services, Consumer Cyclical) entgegen der sonst deutschen Konvention.
13. Uneinheitliche Dezimaldarstellung in Tabelle 3 (−0,6 neben −0,46; 0,1 neben 0,10) und gemischte Schreibungen („z.Bsp.", „zweit stabilste", „Volatilitätsstärkste", „Positiver Tendenz").
14. Fehlendes Abkürzungs-/Symbolverzeichnis bei intensiver Symbolnutzung.

**Einordnung:** Keiner dieser Punkte betrifft die Datenqualität oder die Rechnungen — die Zahlen sind über das Dokument hinweg bemerkenswert konsistent. Es ist ein reines Endredaktionsproblem. Genau deshalb ist es ärgerlich: Eine Stunde Felder-aktualisieren und Korrekturlesen hätte Kategorie A halbiert. In der Bewertung wird dieser Block je nach Prüfer und Raster spürbar gewichtet, weil er die Sorgfalt der *gesamten* Arbeit in Zweifel zieht — zu Unrecht, wie die Datenkonsistenz zeigt, aber der Eindruck entsteht.

---

## 4. Sprachliche Konsistenz und Hinweise auf heterogene Textentstehung

Die Arbeit zerfällt stilistisch erkennbar in drei Schichten:

**Schicht 1 — Kapitel 1 bis 4.2 (und Teile von 3):** funktionale, eher kurzatmige Wissenschaftsprosa mit hoher Fehlerdichte (Genusfehler, Satzabbrüche, Tippfehler, Wiederholungen wie „Die Form der Wolke folgt dem gleichen Strukturmerkmal"). Liest sich wie unter Zeitdruck selbst geschrieben und nicht final redigiert. Charakteristisch: einfache Satzanschlüsse, gelegentliche Umgangsnähe („gefundenes" Vokabular wie „springt", „sticht heraus").

**Schicht 2 — Kapitel 4.3, 5.1, Teile von 6.1:** ruhige, analytisch dichte Passagen mit sauberer Begriffsführung (Strom/Bestand, Markt/Management, mechanische vs. ökonomische Kopplung). Fehlerärmer, aber stilistisch noch mit Schicht 1 verwandt. Vermutlich die am sorgfältigsten selbst überarbeiteten Teile — und qualitativ das Beste der Arbeit.

**Schicht 3 — Kapitel 5.2.2 (Drift-Storylines), 5.2.3/5.2.4 und Teile von 6.2/6.3:** deutlich abweichende Textur. Merkmale: sehr lange, parataktisch gereihte Zahlenketten in fast fehlerfreiem Satzbau; gehäufte Gedankenstrich-Konstruktionen („— eine direkte Konsequenz der regulatorischen Verschärfung"); eine neue Jargonschicht, die vorher nirgends vorkommt („Storylines", „leveragen", „Deleveraging-Pfad", „Marge-Liquidity-Sandwich-Effekt", „Reagierer", „Beobachtungsebenen", „quasi-konstanter Drift"); der Wechsel zu englischen Sektornamen; durchformulierte Mini-Dramaturgien pro Sektor („Die beiden Kurven kreuzen sich um 2013, was den Übergang … markiert").

**Bewertung der KI-Frage, da direkt gestellt:** Beweisen lässt sich Textherkunft von außen nicht, und ich behaupte sie nicht. Aber Schicht 3 trägt mehrere Merkmale, die typisch für maschinell unterstützte oder stark werkzeuggestützte Textproduktion sind (gleichförmige Satzrhythmik, hohe Zahlendichte ohne Stolperer, Gedankenstrich-Stil, Anglizismen-Cluster, abrupt höhere Politur als das Umfeld). Ein Prüfer, der auf Stilbrüche achtet — oder eine Stilometrie-Software einsetzt —, wird genau diese Abschnitte markieren. Zwei praktische Konsequenzen:

1. **Kolloquium:** Die Inhalte von 5.2.2 und 6.2/6.3 müssen zu 100 % beherrscht werden — jede Zahl, jeder Mechanismus, jede Sektor-Storyline. Die wirksamste Entkräftung eines Stilverdachts ist souveräne inhaltliche Hoheit über exakt diese Passagen.
2. **Formales:** Die Eigenständigkeitserklärung nennt „ausdrücklich benannte Quellen und Hilfsmittel". Es lohnt sich, vor dem Kolloquium die aktuell gültige Richtlinie der TH Wildau zum Einsatz von KI-Werkzeugen zu prüfen (viele Hochschulen verlangen seit 2024/25 eine explizite Werkzeugdeklaration) und sich eine ehrliche, vorbereitete Antwort auf die Frage „Welche Hilfsmittel haben Sie wofür eingesetzt?" zurechtzulegen. Diese Frage unvorbereitet zu beantworten ist das größte vermeidbare Risiko der Verteidigung.

Unabhängig von der Herkunft gilt: Der Stilbruch selbst ist ein Mangel an Einheitlichkeit. Eine Schlussredaktion, die Schicht 1 auf das Fehlerniveau von Schicht 3 und Schicht 3 auf die Terminologie von Schicht 1 gebracht hätte, hätte beide Probleme gelöst.

---

## 5. Methodische Kernkritik — die fünf Punkte, an denen ein Prüfer ansetzt

1. **Differenzen-Benchmark / Überdifferenzierung.** Differenzen von (nahezu) unkorrelierten oder messfehlerbehafteten Niveaus erzeugen mechanisch φ → −0,5. Die Profitabilitäts-φ (−0,43 bis −0,46) liegen in dieser Zone; AR(2) mit −0,56 passt zur induzierten MA-Struktur. *Verteidigungslinie:* (a) Die Arbeit deklariert φ explizit als Maß der Veränderungs-Autokorrelation unter einheitlicher Transformation, nicht als Niveau-Persistenz (3.2). (b) Das stärkste Argument steht in den eigenen Daten: Wäre der Wert reine Mechanik, müssten alle sieben Kennzahlen bei −0,5 liegen — Kapitalstruktur liegt bei ≈ 0, Liquidität bei −0,17. Die *Spreizung* zwischen den Kennzahlen ist ökonomisch, selbst wenn das absolute Niveau teilweise mechanisch ist. (c) Fama/French (2000) finden auf Jahresdaten ~38 % Reversion — Größenordnung kompatibel. Diese Argumentation gehört aktiv in die Verteidigung.
2. **Fehlende Stationaritäts- und Spezifikationstests.** Kein ADF/KPSS, keine Residuendiagnostik (Ljung-Box), keine robusten Standardfehler. *Verteidigungslinie:* Parsimonie und Vergleichbarkeit als bewusster Kompromiss (so in 3.2 angelegt); Robustheit über alternative Spezifikationen statt über Tests pro Reihe — vertretbar, aber als Designentscheidung benennen, nicht als Versäumnis stehen lassen.
3. **Querschnittsabhängigkeit.** Gemeinsame Schocks (Krisen, Kap. 5) verletzen die implizite Unabhängigkeitsannahme hinter aggregierten Signifikanzraten. *Verteidigungslinie:* Punktschätzer pro Firma bleiben konsistent; die Arbeit stützt Kernaussagen auf Mediane und Effektstärken, nicht auf die Raten; eine Pesaran-CD-Prüfung wäre der saubere nächste Schritt (Ausblick-Material).
4. **In-Sample-Charakter der Quadranten.** Klassifikation und Krisentest nutzen dieselben Daten. *Verteidigungslinie:* in 5.2.3 bereits selbst benannt — im Kolloquium aktiv ansprechen, bevor es der Prüfer tut, und Out-of-Sample-Split als Future Research skizzieren.
5. **Angekündigte, fehlende Analysen** (Quadranten-Restinformation, Kap.-2-Abschnitte, Ausblick). *Verteidigungslinie:* ehrlich einräumen, und falls die Quadranten-Kontrollvariablen-Regression tatsächlich gerechnet wurde: Ergebnis ins Kolloquium mitbringen. Das wäre die eleganteste Reparatur.

---

## 6. Voraussichtliche Kolloquiumsfragen

Fachlich-methodisch:

1. „Wenn ich weißes Rauschen differenziere, bekomme ich φ = −0,5. Wie viel Ihrer gemessenen Mean-Reversion ist Ökonomie, wie viel Mechanik?" (Antwortgerüst: Punkt 5.1 oben.)
2. „Warum AR(1), wenn AR(2) das R² von 0,19 auf 0,29 hebt?" (Parsimonie; der zweite Lag ändert die Rangordnung der Kennzahlen nicht; Fragestellung zielt auf Korrektur des Vorquartals.)
3. „Sie haben keine Einheitswurzeltests gerechnet. Woher wissen Sie, dass die Differenzen stationär sind — und die Niveaus nicht?"
4. „Ihr Median-Split ist willkürlich. Was passiert bei Terzilen oder bei stetiger Behandlung von φ und σ?"
5. „Was kam bei der in 3.5.3 angekündigten Quadranten-Kontrollvariable heraus?"
6. „Ihre Signifikanzraten ignorieren gemeinsame Schocks über Firmen. Wie verzerrt das Ihre 92 %?"
7. „Tabelle 7 ist mit FCF-Marge überschrieben, zeigt aber die Current Ratio. Welche weiteren Zahlen sollte ich prüfen?" (Unangenehm, aber wahrscheinlich; Antwort: Einzelfehler der Endredaktion, Datenkonsistenz über Kreuzstellen belegen können.)
8. „Warum erklären Strukturmerkmale σ, aber nicht φ? Was ist Ihre ökonomische Theorie dahinter?" (Stärkste Frage zum stärksten Ergebnis — hier kann gepunktet werden: Volatilität ist Exposition gegenüber Schocks und damit strukturell; Korrekturgeschwindigkeit ist Verhaltens-/Governance-getrieben und damit idiosynkratisch.)
9. „Welche praktische Anwendung hat Ihre Taxonomie — Prognose, Screening, Risikomanagement?"
10. „Ihr Sample sind 932 Überlebende. Für wen gelten Ihre Ergebnisse *nicht*?"

Formal/prozessual:

11. „Kapitel 2 kündigt einen Abschnitt zum Beitrag Ihrer Arbeit an, der fehlt. Formulieren Sie ihn jetzt in drei Sätzen."
12. „Welche Hilfsmittel — einschließlich KI-Werkzeugen — haben Sie wofür eingesetzt?"

---

## 7. Gesamtwürdigung und Notentendenz

**Forschungsleistung:** Das Design ist eigenständig komponiert, die Datenarbeit (Filterkette, Ausreißerbehandlung, 100-Quartals-Panel) überdurchschnittlich transparent, das Robustheitsprogramm geht über das übliche Masterniveau hinaus. Die Arbeit findet echte, verteidigbare Ergebnisse — allen voran die σ-φ-Erklärungsasymmetrie — und geht mit Nullergebnissen und Selbstrelativierungen vorbildlich ehrlich um. Die ökonomische Interpretation (4.3) zeigt Verständnis der Mechanik hinter den Zahlen.

**Schwächen:** Das Theoriekapitel ist unfertig, der eigene Beitrag wird nie ausformuliert, FF2 wechselt zwischen Ankündigung und Beantwortung die Gestalt, mehrere angekündigte Analysen fehlen, und das Schlusskapitel liefert keinen Ausblick. Dazu kommt eine Endredaktion, die dem Niveau des Inhalts deutlich hinterherhinkt: tote Querverweise, Satzabbrüche, eine fehlerhafte Hauptgleichung, eine falsch beschriftete Ergebnistabelle und ein hochfrequenter Genusfehler. Schließlich der Stilbruch ab 5.2.2, der unabhängig von seiner Ursache die Einheitlichkeit der Arbeit beschädigt und im Kolloquium Fragen provozieren kann.

**Notentendenz (ausdrücklich unter Vorbehalt — das konkrete Bewertungsraster der TH Wildau und die Gewichtung von Formalia kenne ich nicht, und das Kolloquium geht in der Regel in die Gesamtnote ein):**

- Inhalt/Methodik isoliert: im Bereich 1,7–2,0. Die empirische Substanz, das Robustheitsprogramm und die intellektuelle Ehrlichkeit tragen das.
- Formalia/Struktur isoliert: im Bereich 3,0–3,7. Kategorie-A-Mängel in dieser Häufung sind in den meisten Rastern teuer.
- Realistische Gesamttendenz der schriftlichen Arbeit: **2,0 bei einem inhaltsorientierten Prüfer, 2,3–2,7 bei einem formalstrengen Prüfer.** Ein sehr gutes Kolloquium — insbesondere souveräne Antworten auf die Fragen 1, 5, 8 und 12 — kann das Gesamtbild um eine Drittelnote nach oben verschieben; eine unvorbereitete Antwort auf Frage 12 nach unten.

**Wichtigste Vorbereitung in einem Satz:** Die Verteidigung gewinnt, wer den Differenzen-Benchmark proaktiv entkräftet (Spreizungs-Argument), das fehlende Quadranten-Restinformations-Ergebnis nachliefert und die Hilfsmittel-Frage ruhig und vorbereitet beantwortet.
