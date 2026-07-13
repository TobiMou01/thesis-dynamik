# 2 Theoretische Grundlagen

Dieses Kapitel legt das konzeptuelle und methodische Fundament für die empirische Analyse. Es führt die sieben untersuchten Finanzkennzahlen ein (2.1), entwickelt den theoretischen Rahmen für Mean-Reversion auf Niveaus und Differenzen (2.2), stellt die autoregressiven Modelle und deren Alternativen vor (2.3) und begründet die Quadrantenklassifikation als Typologierahmen (2.4). Das Kapitel beantwortet damit die Frage: Was muss der Leser wissen, um die Methodik in Kapitel 4 und die Ergebnisse in Kapitel 5–7 zu verstehen?

## 2.1 Finanzkennzahlen und ihre ökonomische Bedeutung

### Die sieben Kennzahlen

Die vorliegende Arbeit untersucht sieben Finanzkennzahlen, die drei fundamentale Dimensionen der Unternehmensperformance abdecken: Profitabilität, Liquidität und Kapitalstruktur. Tabelle 2.1 stellt die Kennzahlen mit ihren Berechnungsformeln und der jeweiligen ökonomischen Aussage dar.

**Tabelle 2.1:** Die sieben untersuchten Finanzkennzahlen

| Kennzahl | Formel | Ökonomische Aussage |
|---|---|---|
| ROA | Nettoergebnis / Bilanzsumme | Gesamtkapitalrentabilität: Wie effizient setzt das Unternehmen sein gesamtes Kapital ein? |
| ROE | Nettoergebnis / Eigenkapital | Eigenkapitalrentabilität: Welche Rendite erwirtschaftet das Unternehmen für seine Eigentümer? |
| EBIT-Marge | EBIT / Umsatz | Operative Profitabilität: Welcher Anteil des Umsatzes verbleibt als operativer Gewinn? |
| FCF-Marge | Free Cashflow / Umsatz | Cashflow-Generierung: Wie viel frei verfügbarer Cashflow entsteht pro Umsatzeinheit? |
| Current Ratio | Umlaufvermögen / kurzfr. Verbindlichkeiten | Kurzfristige Zahlungsfähigkeit: Kann das Unternehmen seine kurzfristigen Verpflichtungen decken? |
| Debt-to-Equity | Fremdkapital / Eigenkapital | Verschuldungsgrad: Wie stark ist das Unternehmen fremdfinanziert? |
| Eigenkapitalquote | Eigenkapital / Bilanzsumme | Eigenfinanzierungsgrad: Welcher Anteil der Bilanzsumme ist eigenfinanziert? |

Die Auswahl deckt bewusst verschiedene Ebenen des Abschlusses ab: Die Profitabilitätskennzahlen (ROA, ROE, EBIT-Marge, FCF-Marge) stammen primär aus der Gewinn- und Verlustrechnung bzw. der Kapitalflussrechnung, die Current Ratio aus dem kurzfristigen Bereich der Bilanz, und die Kapitalstruktur-Kennzahlen (Debt-to-Equity, Eigenkapitalquote) aus der langfristigen Bilanzstruktur. Diese Heterogenität ist beabsichtigt, da die Arbeit gerade die Frage untersucht, ob Kennzahlen aus unterschiedlichen Abschlussbereichen systematisch verschiedene Dynamikmuster aufweisen.

### Drei Kategorien und ihre ökonomische Logik

Die sieben Kennzahlen lassen sich auf Basis ihrer ökonomischen Treiber in drei Kategorien einteilen, die sich fundamental in ihren Veränderungsmechanismen unterscheiden:

**Profitabilität (ROA, ROE, EBIT-Marge, FCF-Marge):** Profitabilitätskennzahlen sind primär marktgetrieben. Umsatz und Kosten schwanken mit Nachfrage, Wettbewerbsintensität und Konjunkturzyklus. Quartalsveränderungen enthalten regelmäßig temporäre Effekte — ein außergewöhnlich starkes Quartal durch Einmalaufträge, Saisonspitzen oder Kosteneinsparungsprogramme wird typischerweise im Folgequartal nicht in gleicher Höhe wiederholt. Die ökonomische Theorie prognostiziert daher eine systematische Rückbildung überdurchschnittlicher Veränderungen: Wettbewerb erodiert übernormale Renditen, und Einmaleffekte verschwinden definitionsgemäß (Fama & French, 2000). Die FCF-Marge nimmt innerhalb der Profitabilitätskennzahlen eine besondere Stellung ein, da sie ausschließlich zahlungswirksame Größen erfasst und damit die periodengerechte Abgrenzung (Accruals) umgeht. Dichev und Tang (2009) zeigen, dass gerade der Accrual-Anteil von Earnings eine geringere Persistenz aufweist als die Cashflow-Komponente — ein Befund, der die Differenzierung innerhalb der Profitabilitätsgruppe motiviert.

**Liquidität (Current Ratio):** Die Current Ratio nimmt eine hybride Position ein. Einerseits ist sie operativ bestimmt — Lagerzyklen, Zahlungsziele und saisonale Umsatzschwankungen beeinflussen das Umlaufvermögen und die kurzfristigen Verbindlichkeiten unmittelbar. Andererseits unterliegt sie auch Managemententscheidungen, etwa über Kreditlinien, Working-Capital-Programme oder das Timing von Lieferantenzahlungen. Diese Mischung aus exogenen Markteinflüssen und endogener Steuerung lässt eine mittlere Veränderungsdynamik erwarten — volatiler als reine Bilanzstrukturkennzahlen, aber weniger stark korrigierend als Profitabilitätsmaße. Eljelly (2004) dokumentiert den grundsätzlichen Zielkonflikt zwischen Liquidität und Profitabilität und zeigt, dass Unternehmen ihre Liquiditätsposition aktiver steuern als oft angenommen.

**Kapitalstruktur (Debt-to-Equity, Eigenkapitalquote):** Kapitalstruktur-Kennzahlen sind primär managementgesteuert. Finanzierungsentscheidungen — Anleiheemissionen, Kredittilgungen, Aktienrückkäufe, Kapitalerhöhungen — sind diskrete Ereignisse, keine kontinuierlichen Prozesse. Die Eigenkapitalquote eines Unternehmens ändert sich typischerweise nur dann substantiell, wenn eine bewusste Finanzierungsentscheidung getroffen wird. Zwischen solchen Entscheidungen ist die Quartalsveränderung nahezu null. Die Theorie der Kapitalstruktur (beginnend mit Modigliani und Miller, 1958, und deren Erweiterungen) legt nahe, dass Unternehmen eine Zielkapitalstruktur anstreben und Abweichungen davon langsam korrigieren — ein Prozess, der sich in hoher Niveaupersistenz, aber geringer Quartalsdynamik äußert.

Diese theoretische Dreiteilung — marktgetrieben, hybrid, managementgesteuert — bildet die Grundlage für die empirische Analyse in Kapitel 5, die zeigt, dass sich die drei Kategorien tatsächlich in einer konsistenten Drei-Schichten-Hierarchie der Veränderungsdynamik manifestieren (vgl. Abbildung 2.1).

![Abb. 2.1: Drei-Schichten-Hierarchie der Kennzahlendynamik. Die Korrekturintensität der Quartalsveränderungen nimmt von Profitabilität (starke Mean-Reversion) über Liquidität (mittlere Dynamik) bis Kapitalstruktur (kaum Korrektur) systematisch ab.](Kapitel_2_Grafiken/abb_2_4_drei_schichten.png)

### DuPont-Zerlegung und mechanische Wechselwirkungen

Die sieben Kennzahlen sind nicht unabhängig voneinander. Die DuPont-Zerlegung (Nissim & Penman, 2001) macht die zentrale mechanische Verknüpfung explizit:

$$ROE = ROA \times \frac{\text{Bilanzsumme}}{\text{Eigenkapital}} = ROA \times (1 + D/E)$$

ROE ist also das Produkt aus der Gesamtkapitalrentabilität und dem Leverage-Faktor. Diese Formelbeziehung hat eine direkte Konsequenz für die Dynamikanalyse: Veränderungen im ROE können sowohl aus Profitabilitätsänderungen (Zähler) als auch aus Leverage-Änderungen (Nenner) resultieren. Da ROE und Debt-to-Equity denselben Nenner teilen (Eigenkapital), entsteht eine mechanische Volatilitätskopplung, die sich in einer hohen Korrelation der Veränderungsvolatilitäten zwischen ROE und D/E niederschlägt (vgl. Kapitel 6). Diese Kopplung ist keine ökonomische Erkenntnis, sondern eine Formelkonsequenz — eine Unterscheidung, die bei der Interpretation der Interdependenzergebnisse (FF2) zentral ist.

![Abb. 2.2: DuPont-Zerlegung und mechanische Kopplung. ROE als Produkt von ROA und Leverage-Faktor. Die gemeinsame Abhängigkeit vom Eigenkapital erzeugt eine mechanische Volatilitätskopplung zwischen ROE und D/E.](Kapitel_2_Grafiken/abb_2_5_dupont_zerlegung.png)

## 2.2 Mean-Reversion in der Finanztheorie

### Das Konzept

Mean-Reversion bezeichnet die Tendenz einer ökonomischen Variablen, nach Abweichungen vom langfristigen Gleichgewicht zu diesem zurückzukehren. In der Finanztheorie hat das Konzept eine ökonomische Begründung, die über rein statistische Regelmäßigkeit hinausgeht: Überdurchschnittliche Renditen ziehen Wettbewerber an, die den Vorteil erodieren; Kostenineffizienzen werden durch Managementmaßnahmen korrigiert; regulatorische Vorgaben erzwingen Anpassungen bei Kennzahlen wie der Eigenkapitalquote. Fama und French (2000) dokumentieren diese Mean-Reversion für Profitabilitätskennzahlen auf Unternehmensebene und zeigen, dass sowohl die Geschwindigkeit als auch die Stärke der Rückkehr zwischen Unternehmen und Branchen variiert.

### Niveaupersistenz vs. Veränderungskorrektur — der theoretische Kernpunkt

Die vorliegende Arbeit unterscheidet fundamental zwischen zwei Formen der Mean-Reversion, die in der Literatur häufig vermischt werden:

**Mean-Reversion auf Niveaus** beschreibt die klassische Frage: Kehrt der ROA eines Unternehmens nach einem Einbruch wieder zum langfristigen Mittelwert zurück? Das zugehörige Modell ist $Y(t) = c + \varphi_1 \cdot Y(t-1) + \varepsilon(t)$, wobei $\varphi_1$ die Niveaupersistenz misst. Ein $\varphi_1$ nahe 1 bedeutet: Das aktuelle Niveau ist fast vollständig durch das vorherige bestimmt — die Kennzahl ist träge. Ein $\varphi_1$ deutlich unter 1 bedeutet: Abweichungen vom Mittelwert werden teilweise korrigiert.

**Mean-Reversion der Veränderungen** — der Ansatz dieser Arbeit — fragt stattdessen: Wenn der ROA im letzten Quartal um 2 Prozentpunkte gestiegen ist, steigt er dann im nächsten Quartal nochmals, oder korrigiert sich die Veränderung? Das Modell ist $\Delta Y(t) = c + \varphi_1 \cdot \Delta Y(t-1) + \varepsilon(t)$, wobei ein negatives $\varphi_1$ bedeutet, dass eine überdurchschnittliche Quartalsveränderung im Folgequartal teilweise rückgängig gemacht wird.

Die Unterscheidung ist nicht nur semantisch, sondern führt zu komplementären Einsichten. Abbildung 2.1 illustriert den Unterschied am Beispiel des ROA von Procter & Gamble: Das Niveau (oberer Plot) zeigt moderate Schwankungen um einen Mittelwert von 0,024 — es ist persistent, aber nicht konstant. Die ersten Differenzen (unterer Plot) zeigen dagegen ein charakteristisches Zickzack-Muster um null, bei dem auf positive Veränderungen häufig negative folgen und umgekehrt. Dieses Korrekturmuster ist der empirische Ausdruck eines negativen $\varphi_1$ auf Differenzen.

![Abb. 2.3: Niveaus vs. erste Differenzen am Beispiel ROA (Procter & Gamble, 100 Quartale). Oberer Plot: Das ROA-Niveau schwankt um den Mittelwert (0,024), mit moderater Persistenz. Unterer Plot: Die Quartalsveränderungen ΔROA oszillieren um null mit einem sichtbaren Korrekturmuster — auf positive Ausschläge folgen häufig negative.](Kapitel_2_Grafiken/abb_2_1_niveaus_vs_differenzen.png)

Die empirischen Daten dieser Arbeit zeigen, dass beide Perspektiven zusammen ein vollständigeres Bild ergeben als jede einzeln: Die Eigenkapitalquote hat eine sehr hohe Niveaupersistenz, aber nahezu keine Autokorrelation der Veränderungen. Ökonomisch bedeutet das: Das Eigenkapitalniveau ändert sich kaum, und wenn es sich ändert, ist die Richtung der nächsten Änderung unvorhersagbar. Der ROA zeigt das umgekehrte Muster: Moderate Niveaupersistenz, aber starke Veränderungskorrektur. Das Niveau schwankt, aber die Schwankungen korrigieren sich systematisch. Abbildung 2.4 veranschaulicht diese beiden Dynamiktypen konzeptuell (die konkreten Parameterwerte folgen in Kapitel 5).

![Abb. 2.4: Konzeptuelle Darstellung der beiden Mean-Reversion-Formen. Links: Niveaupersistenz (φ₁ ≈ 0,93) — das Niveau driftet langsam, typisch für Kapitalstruktur. Rechts: Veränderungskorrektur (φ₁ ≈ −0,43) — auf jeden Ausschlag folgt eine Gegenreaktion, typisch für Profitabilität.](Kapitel_2_Grafiken/abb_2_2_mean_reversion_konzept.png)

### Stationarität und die Wahl erster Differenzen

Die Modellierung auf ersten Differenzen hat neben der inhaltlichen Motivation auch eine technische Begründung: Erste Differenzen stellen Stationarität sicher, ohne Annahmen über die Integrationsordnung der Niveaus treffen zu müssen. Kapitalstruktur-Kennzahlen mit $\varphi_{1,\text{levels}}$ nahe 1 sind potenziell einheitswurzelnah, was OLS-Schätzer auf Niveaus verzerren kann (Hamilton, 1994). Die Differenzenbildung löst dieses Problem, führt aber zu einem Trade-off: Saisonale Muster (etwa höhere Q4-Umsätze im Einzelhandel) werden durch $\Delta Y = Y(t) - Y(t-1)$ nicht eliminiert, sondern nur zeitlich verschoben. Saisonale Differenzen ($\Delta_4 Y = Y(t) - Y(t-4)$) adressieren diesen Punkt und dienen als Robustheitscheck (vgl. Abschnitt 4.4).

Die Wahl einer einheitlichen Transformation (erste Differenzen) für alle sieben Kennzahlen stellt einen bewussten Trade-off zwischen statistischer Optimalität und Vergleichbarkeit dar: Metrisch-spezifische Transformationen — etwa saisonale Differenzen für die Current Ratio oder Level-Modelle für die Eigenkapitalquote — würden die individuelle Modellanpassung verbessern, aber den querschnittlichen Vergleich der $\varphi_1$-Koeffizienten zwischen Kennzahlen unmöglich machen. Da die Forschungsfrage FF1 genau nach diesem Vergleich fragt, ist die einheitliche Transformation notwendig (vgl. Abschnitt 4.4 für die detaillierte methodische Diskussion).

## 2.3 Autoregressive Modelle

### Das AR(1)-Modell als Werkzeug

Das autoregressive Modell erster Ordnung ist das einfachste Zeitreihenmodell, das eine Ein-Schritt-Autokorrelation erfasst. In der Anwendung auf erste Differenzen lautet es:

$$\Delta Y_{ik}(t) = c_{ik} + \varphi_{1,ik} \cdot \Delta Y_{ik}(t-1) + \varepsilon_{ik}(t)$$

wobei $i$ das Unternehmen, $k$ die Kennzahl, $c_{ik}$ die Drift-Konstante, $\varphi_{1,ik}$ den Autokorrelationskoeffizienten und $\varepsilon_{ik}(t) \sim WN(0, \sigma^2)$ den Fehlerterm bezeichnet. Die Schätzung wird individuell per OLS für jede Unternehmen-Kennzahl-Kombination durchgeführt — ein Designprinzip, das in Abschnitt 4.2 ausführlich begründet wird (Pesaran & Smith, 1995).

Das Modell liefert zwei Schlüsselgrößen pro Schätzung:

Der **Mean-Reversion-Koeffizient $\varphi_1$** misst, welcher Anteil einer Quartalsveränderung im Folgequartal rückgängig gemacht wird. Bei einem hypothetischen $\varphi_1 = -0{,}40$ bedeutet das: Ein Unternehmen, dessen ROA im letzten Quartal um 1 Prozentpunkt gestiegen ist, wird im nächsten Quartal ceteris paribus eine Veränderung von $-0{,}40$ Prozentpunkten zeigen — die Veränderung korrigiert sich teilweise. Bei $\varphi_1 \approx 0$ ist die aktuelle Veränderung unkorreliert mit der vorherigen — das Modell hat keine Vorhersagekraft.

Die **Veränderungsvolatilität $\sigma(\Delta Y)$** ist die Standardabweichung der gesamten Differenzenreihe und misst, wie stark eine Kennzahl typischerweise von Quartal zu Quartal schwankt. Sie ist bewusst als Gesamtvolatilität der transformierten Reihe definiert, nicht als Residualvolatilität des AR-Modells.

### Vier Modellvarianten

Neben dem Hauptmodell (diff1) werden drei alternative Spezifikationen geschätzt, die jeweils eine andere Perspektive auf die Kennzahlen-Dynamik einnehmen:

Die **Levels-Variante** $Y(t) = c + \varphi_1 \cdot Y(t-1) + \varepsilon(t)$ beantwortet die komplementäre Frage nach der Niveaupersistenz. Zusammen mit dem Hauptmodell ergibt sich ein konsistentes Bild: Kennzahlen mit hohem $\varphi_{1,\text{levels}}$ und niedrigem $|\varphi_{1,\text{diff}}|$ — wie die Eigenkapitalquote — haben ein persistentes Niveau mit zufälligen Quartalsänderungen. Kennzahlen mit niedrigerem $\varphi_{1,\text{levels}}$ und stark negativem $\varphi_{1,\text{diff}}$ — wie der ROA — haben ein schwankendes Niveau mit systematisch korrigierenden Veränderungen.

Das **AR(2)-Modell** $\Delta Y(t) = c + \varphi_1 \cdot \Delta Y(t-1) + \varphi_2 \cdot \Delta Y(t-2) + \varepsilon(t)$ testet, ob ein einzelner Lag die Autokorrelationsstruktur ausreichend erfasst oder ob ein längeres Gedächtnis besteht.

Die **saisonale Variante** bildet zunächst die Differenz $\Delta_4 Y(t) = Y(t) - Y(t-4)$ (Vergleich mit dem Vorjahresquartal) und schätzt darauf ein AR(1)-Modell. Sie eliminiert saisonale Muster und prüft, ob die negativen $\varphi_1$-Werte auf ersten Differenzen teilweise saisonale Artefakte sind.

Alle vier Varianten dienen gemeinsam der Robustheitsprüfung. Die zentrale Hypothese lautet: Wenn die Drei-Schichten-Hierarchie (Profitabilität > Liquidität > Kapitalstruktur in der Korrekturgeschwindigkeit) unter allen vier Spezifikationen in ihrer Rangordnung stabil bleibt, ist sie eine robuste Eigenschaft der Daten und kein Artefakt der Transformationswahl. Die Ergebnisse in Kapitel 5 bestätigen diese Hypothese.

### Warum AR(1) und nicht komplexere Modelle?

Die Entscheidung für AR(1) als Hauptmodell folgt dem Parsimonie-Prinzip, ist aber auch inhaltlich begründet. Drei alternative Modellklassen wurden erwogen und begründet verworfen:

**VAR-Modelle** (Love & Zicchino, 2006) würden die simultane Dynamik mehrerer Kennzahlen innerhalb eines Unternehmens modellieren. Die empirischen Ergebnisse zeigen jedoch, dass die querschnittlichen Korrelationen der $\varphi_1$-Koeffizienten zwischen Kennzahlenkategorien sehr gering sind ($|\rho| < 0{,}10$; vgl. Kapitel 6). Ein VAR-Modell würde daher primär Rauschen modellieren und wäre bei 7 Kennzahlen und 100 Quartalen mit einer hohen Parameteranzahl überidentifiziert.

**GARCH-Modelle** adressieren die bedingte Varianz, nicht den bedingten Mittelwert. Die Forschungsfrage dieser Arbeit zielt auf die Autokorrelation der *Mittelwerte* der Veränderungen ($\varphi_1$), nicht auf die Volatilitätsdynamik. GARCH und AR(1) beantworten verschiedene Fragen. Zusätzlich zeigen empirische Tests, dass die ARCH-LM-Voraussetzungen bei Quartalsdaten von Finanzkennzahlen nur bei 23–42 % der Unternehmen erfüllt sind.

**Strukturbruchmodelle** setzen ex ante definierte Bruchpunkte voraus oder schätzen diese datengetrieben. Die Event-Analyse in Kapitel 6 (FF2) adressiert Strukturbrüche auf eine komplementäre Weise: Hochvolatilitätsphasen werden datengetrieben identifiziert, und die Reaktionen verschiedener Dynamik-Typen werden verglichen — ohne parametrische Annahmen über die Bruchstruktur.

## 2.4 Quadrantenklassifikation als Typologierahmen

### Zwei Dimensionen, vier Dynamiktypen

Die AR(1)-Schätzung liefert für jedes Unternehmen-Kennzahl-Paar zwei Parameter: den Mean-Reversion-Koeffizienten $\varphi_1$ und die Veränderungsvolatilität $\sigma(\Delta Y)$. Diese beiden Größen messen konzeptuell verschiedene Eigenschaften: $\varphi_1$ erfasst die Vorhersagbarkeit der Veränderungsrichtung (korrigiert sich eine Veränderung oder bleibt sie bestehen?), während $\sigma(\Delta Y)$ die Magnitude der Veränderungen misst (wie groß sind die typischen Quartalsschwankungen?). Die empirische Analyse in Kapitel 7 bestätigt diese konzeptuelle Trennung: $\sigma$ ist stark größenabhängig, während $\varphi_1$ keinen konsistenten Zusammenhang mit der Unternehmensgröße zeigt. Die Dimensionen haben also unterschiedliche externe Treiber.

Die Kombination beider Dimensionen über einen Median-Split ergibt vier Quadranten, die in Abbildung 2.3 als Typologierahmen dargestellt sind.

![Abb. 2.5: Quadrantenklassifikation als Dynamik-Typologierahmen. Die vertikale Achse (φ₁) differenziert zwischen korrektiven und persistenten Veränderungsmustern; die horizontale Achse (σ) zwischen stabilen und volatilen Kennzahlen. Jeder Quadrant beschreibt einen ökonomisch interpretierbaren Dynamiktyp.](Kapitel_2_Grafiken/abb_2_3_quadrantenschema.png)

**Korrektiv-Stabil** (stark negatives $\varphi_1$, niedriges $\sigma$): Veränderungen sind klein und korrigieren sich systematisch. Typisch für reife, diversifizierte Unternehmen in stabilen Branchen, deren Profitabilitätskennzahlen eng um einen Gleichgewichtswert schwanken.

**Korrektiv-Volatil** (stark negatives $\varphi_1$, hohes $\sigma$): Große Ausschläge, die sich aber systematisch zurückbilden. Typisch für zyklische Branchen, in denen Nachfrageschwankungen starke Quartalseffekte erzeugen, die durch Wettbewerbs- und Anpassungsmechanismen korrigiert werden.

**Persistent-Stabil** (nahe null $\varphi_1$, niedriges $\sigma$): Kaum Veränderung, und was sich ändert, bleibt bestehen. Typisch für Kapitalstruktur-Kennzahlen reifer Unternehmen — die Eigenkapitalquote ändert sich selten, aber wenn sie sich ändert (etwa durch eine Akquisition), bleibt das neue Niveau dauerhaft.

**Persistent-Volatil** (nahe null $\varphi_1$, hohes $\sigma$): Große Schwankungen ohne systematische Korrektur. Das aus Analysesicht problematischste Profil, da weder die Richtung noch die Stärke der Veränderungen vorhersagbar ist.

### Median-Split: Begründung und Einschränkungen

Der Median-Split als Trennmechanismus ist eine methodische Entscheidung, deren Vor- und Nachteile transparent zu benennen sind. MacCallum, Zhang, Preacher und Rucker (2002) kritisieren die Dichotomisierung kontinuierlicher Variablen grundsätzlich und schätzen den Informationsverlust auf etwa 20 % der Parametergenauigkeit. Rucker, McShane und Preacher (2015) relativieren diese Kritik und zeigen, dass Median-Splits dann akzeptabel sind, wenn die beiden dichotomisierten Variablen gering korreliert sind — eine Bedingung, die hier weitgehend erfüllt ist ($|\rho| < 0{,}19$ für Profitabilitätskennzahlen).

Drei Argumente sprechen für den Median-Split: Erstens die Interpretierbarkeit — die Labels sind direkt aus den Dimensionen abgeleitet. Zweitens die Transparenz — die Zuordnung ist vollständig nachvollziehbar und reproduzierbar. Drittens die Analogie zur Portfolio-Sort-Methodik, die in der empirischen Finanzforschung seit Fama und French (1993) als Standardwerkzeug etabliert ist.

Die Einschränkung liegt in der willkürlichen Grenzziehung: Ein Unternehmen mit $\varphi_1 = -0{,}44$ (knapp unter dem Median) und eines mit $\varphi_1 = -0{,}42$ (knapp darüber) werden unterschiedlichen Quadranten zugewiesen, obwohl der inhaltliche Unterschied minimal ist. Diese Limitation wird durch eine K-Means-Clusteranalyse als datengetriebenen Robustheitscheck adressiert (vgl. Kapitel 7).

### Empirische Trennbarkeit der Dimensionen

Eine zentrale Voraussetzung für die Sinnhaftigkeit der Quadrantenklassifikation ist die empirische Unabhängigkeit von $\varphi_1$ und $\sigma(\Delta Y)$. Theoretisch könnte höhere Volatilität automatisch stärkere Mean-Reversion erzeugen, etwa weil große Ausschläge häufiger zu Umkehrungen führen. Die empirische Prüfung über Spearman-Rangkorrelationen zeigt, dass die Korrelation für alle sieben Kennzahlen schwach ist: $|\rho| < 0{,}19$ für die vier Profitabilitätskennzahlen und $|\rho| < 0{,}25$ für alle Kennzahlen (vgl. Tabelle 4.3 in Kapitel 4 für die vollständige Aufstellung). Die Dimensionen sind empirisch trennbar, und die Quadrantenklassifikation nutzt tatsächlich zwei weitgehend unabhängige Informationsdimensionen.

---

*Nachdem dieses Kapitel die theoretischen Konzepte — Kennzahlenkategorien, Mean-Reversion, autoregressive Modelle und Quadrantenklassifikation — eingeführt hat, ordnet das folgende Kapitel 3 die vorliegende Arbeit in den Stand der Forschung ein und identifiziert die Forschungslücke, die durch die drei Forschungsfragen adressiert wird.*
