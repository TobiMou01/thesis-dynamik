# 6 Ergebnisse FF2: Interdependenzen und zeitliche Manifestation

FF2 untersucht, wie die Dynamikmuster der sieben Kennzahlen zusammenhängen und ob die Quadrantenklassifikation prädiktive Kraft für das Verhalten in Stressphasen hat. Die Analyse gliedert sich in zwei konzeptionell verschiedene Teile: Abschnitt 6.1 erläutert die FF2-spezifische Methodik. Abschnitt 6.2 analysiert die querschnittliche Interdependenz — hängen die Dynamikmuster verschiedener Kennzahlen innerhalb eines Unternehmens zusammen? Abschnitt 6.3 untersucht die zeitliche Manifestation — reagieren verschiedene Dynamiktypen unterschiedlich auf exogene Schocks? Abschnitt 6.4 fasst die Befunde zusammen.

## 6.1 Methodik

### Querschnittsanalyse

Die querschnittliche Interdependenz wird über drei komplementäre Maße quantifiziert. Die Spearman-Rangkorrelation der $\varphi_1$-Werte zwischen Kennzahlenpaaren (21 Paare bei 7 Kennzahlen) misst, ob Unternehmen mit starker ROA-Mean-Reversion auch starke ROE- oder EBIT-Mean-Reversion zeigen. Die analoge Korrelation der $\sigma(\Delta Y)$-Werte misst den Zusammenhang der Veränderungsvolatilitäten. Cramér's V auf $4 \times 4$-Kontingenztafeln der Quadrantenzuordnungen quantifiziert die Übereinstimmung der diskreten Klassifikation.

Die Verwendung von Spearman statt Pearson ist methodisch begründet: Die $\varphi_1$-Verteilungen sind für einige Kennzahlen (insbesondere D/E und Eigenkapitalquote) nicht normalverteilt und enthalten Ausreißer, die Pearson-Korrelationen verzerren würden. Cramér's V ist als Effektstärkemaß für kategoriale Variablen der Standard und wird hier für die Quadrantenüberschneidungen verwendet — konsistent mit der Stollhoff-Entscheidung, Cramér's V für diskrete Daten (FF3) einzusetzen.

### Event-Analyse

Die zeitliche Manifestation wird über datengetriebene Peak-Identifikation analysiert. Ein Quartal gilt als Peak-Window, wenn mindestens drei der sieben Kennzahlen gleichzeitig das 90. Perzentil der rollierenden Querschnittsvolatilität überschreiten. Dieser Ansatz vermeidet die willkürliche Ex-ante-Datierung von Krisen und identifiziert nur Phasen, die sich tatsächlich in den Finanzkennzahlen niederschlagen. Die Reaktionsunterschiede zwischen Quadranten werden deskriptiv über Median-Vergleiche dargestellt; bei Bedarf können nicht-parametrische Tests (Mann-Whitney U, Kruskal-Wallis) mit Bonferroni-Korrektur die statistische Signifikanz bestätigen.

## 6.2 Querschnittliche Interdependenz

### Die $\varphi_1$-Korrelationsmatrix

Abbildung 6.1 zeigt die Spearman-Rangkorrelationen der $\varphi_1$-Koeffizienten zwischen allen Kennzahlenpaaren. Das Muster ist eindeutig: Die Korrelationen konzentrieren sich auf den Profitabilitätsblock, während die kategorie-übergreifenden Zusammenhänge vernachlässigbar sind.

![Abb. 6.1: Spearman-Korrelationsmatrix der φ₁-Koeffizienten. Die Profitabilitätskennzahlen (oberer linker Block) zeigen starke interne Korrelationen (ρ = 0,50–0,78), während alle cross-kategorialen Korrelationen unter 0,10 liegen. Die Drei-Schichten-Hierarchie manifestiert sich als Blockstruktur.](Kapitel_6_Grafiken/abb_6_1_phi1_korrelationsmatrix.png)

**Befund 1 — Blockstruktur der Profitabilität:** Die drei buchhalterischen Profitabilitätskennzahlen bilden einen kohärenten Block: ROA $\times$ ROE ($\rho = 0{,}78$), ROA $\times$ EBIT-Marge ($\rho = 0{,}54$), ROE $\times$ EBIT-Marge ($\rho = 0{,}50$). Ein Unternehmen mit starker ROA-Veränderungskorrektur zeigt mit hoher Wahrscheinlichkeit auch starke ROE- und EBIT-Margen-Korrektur. Die ökonomische Erklärung: Alle drei Kennzahlen werden durch dieselben operativen Treiber bestimmt — Umsatzschwankungen, Kostenentwicklung, Einmaleffekte —, die sich in allen drei Maßen gleichzeitig niederschlagen.

**Befund 2 — FCF als Sonderfall:** Die FCF-Marge korreliert schwächer mit den anderen Profitabilitätskennzahlen ($\rho = 0{,}15$ bis $0{,}20$) als diese untereinander. Das ist ökonomisch erklärbar: Die FCF-Marge ist eine Cashflow-basierte, keine buchhalterische Kennzahl. Dechow (1994) zeigt, dass Accrual-Timing die Autokorrelationsstruktur von Earnings verändert, ohne die grundlegende Mean-Reversion-Tendenz zu beseitigen. Die FCF-Marge teilt die *Stärke* der Mean-Reversion mit den buchhalterischen Kennzahlen ($\varphi_1 \approx -0{,}46$), aber die *individuellen Profile* — welche Unternehmen besonders stark oder schwach korrigieren — sind weniger gekoppelt.

**Befund 3 — Schichtübergreifende Unabhängigkeit:** Alle 15 cross-kategorialen $\varphi_1$-Korrelationen liegen unter $|\rho| < 0{,}10$. Die Korrekturgeschwindigkeit der Profitabilität sagt nichts über die Korrekturgeschwindigkeit der Kapitalstruktur aus — und umgekehrt. Die Drei-Schichten-Hierarchie aus FF1 ist damit nicht nur eine Rangordnung der Median-$\varphi_1$-Werte, sondern reflektiert tatsächlich separable Dimensionen der Unternehmensdynamik.

### Die $\sigma$-Korrelationsmatrix — ein anderes Muster

Die Korrelationen der Veränderungsvolatilitäten zeigen ein fundamental anderes Muster als die $\varphi_1$-Korrelationen. Abbildung 6.2 macht den Kontrast sichtbar.

![Abb. 6.2: Spearman-Korrelationsmatrix der σ(ΔY)-Werte. Im Gegensatz zur φ₁-Matrix zeigen sich starke cross-kategoriale Kopplungen, insbesondere ROE × D/E (ρ = 0,82) und EBIT × FCF (ρ = 0,78). Die Volatilitäten sind stärker vernetzt als die Korrekturgeschwindigkeiten.](Kapitel_6_Grafiken/abb_6_2_sigma_korrelationsmatrix.png)

**Befund 4 — ROE $\times$ D/E: Mechanische Volatilitätskopplung ($\rho_\sigma = 0{,}82$).** Dies ist die stärkste bivariate Korrelation im gesamten Datensatz. Sie steht in scharfem Kontrast zur $\varphi_1$-Korrelation derselben Kennzahlen ($\rho_{\varphi_1} = 0{,}07$). Die Erklärung ist die DuPont-Zerlegung (Nissim & Penman, 2001; vgl. Abschnitt 2.1): ROE $= \text{ROA} \times (1 + D/E)$. Da ROE und D/E denselben Nenner (Eigenkapital) teilen, erzeugt jede Eigenkapitalveränderung eine mechanische Co-Bewegung der Volatilitäten beider Kennzahlen. Christie (1982) dokumentiert diesen Leverage-Effekt auf Aktienebene — die vorliegenden Ergebnisse zeigen ihn auf Kennzahlenebene.

Die Implikation ist methodisch bedeutsam: Hohe $\sigma$-Korrelation zwischen ROE und D/E ist kein Hinweis auf eine ökonomische Interdependenz der Dynamikmuster, sondern eine Formelkonsequenz. Bei der Interpretation der Volatilitätszusammenhänge muss zwischen mechanischen und ökonomischen Kopplungen unterschieden werden.

**Befund 5 — EBIT-Marge $\times$ FCF-Marge ($\rho_\sigma = 0{,}78$, $\rho_{\varphi_1} = 0{,}15$).** Beide Kennzahlen teilen den Umsatznenner und überlappen teilweise im Zähler (operatives Ergebnis vs. operativer Cashflow). Unternehmen mit volatilen Margen haben daher auch volatile Cashflows. Die schwache $\varphi_1$-Korrelation zeigt jedoch: Die *Autokorrelationsstruktur* — also wie schnell sich Veränderungen korrigieren — ist verschieden. Das Accrual-Timing (Dechow, 1994) glättet die EBIT-Marge relativ zum Cashflow und verändert damit die Korrekturstruktur, ohne die Volatilität substantiell zu reduzieren.

**Befund 6 — Die Eigenkapitalquote als Brücke.** Die Eigenkapitalquote korreliert in $\sigma$ sowohl mit Profitabilität (ROA: $\rho = 0{,}57$) als auch mit Liquidität (CR: $\rho = 0{,}34$) und Kapitalstruktur (D/E: $\rho = 0{,}29$). Sie ist die einzige Kennzahl mit Volatilitätszusammenhängen über alle drei Schichten hinweg — ökonomisch plausibel, weil die Eigenkapitalquote als Bilanzstrukturkennzahl sowohl von der Ergebnisseite (Gewinnthesaurierung) als auch von der Finanzierungsseite (Kapitalmaßnahmen) beeinflusst wird.

### $\varphi_1$ versus $\sigma$: Zwei verschiedene Informationsdimensionen

![Abb. 6.3: φ₁-Korrelation vs. σ-Korrelation für alle 21 Kennzahlenpaare. Punkte oberhalb der Diagonalen zeigen Paare, bei denen die Volatilitätskopplung stärker ist als die Korrektur-Kopplung. Die mechanische ROE × D/E-Kopplung (rot) ist der extremste Fall: nahezu keine φ₁-Korrelation bei maximaler σ-Korrelation.](Kapitel_6_Grafiken/abb_6_3_phi1_vs_sigma_vergleich.png)

Abbildung 6.3 bringt den zentralen Befund auf den Punkt: Die Mehrheit der Kennzahlenpaare liegt oberhalb der Diagonalen — die Volatilitäten sind stärker vernetzt als die Korrekturgeschwindigkeiten. $\sigma$ misst, *wie stark* ein Unternehmen schwankt, und wird durch Unternehmensgröße, Geschäftsmodell und Branche bestimmt — Faktoren, die auf mehrere Kennzahlen gleichzeitig wirken. $\varphi_1$ misst, *wie schnell* sich Veränderungen korrigieren, und wird durch kennzahlspezifische Mechanismen bestimmt — Wettbewerbsdruck bei Profitabilität, Managemententscheidungen bei Kapitalstruktur. Die Dimensionen haben also verschiedene Treiber, was ihre empirische Trennbarkeit in der Quadrantenklassifikation erklärt.

### Quadrantenüberschneidungen (Cramér's V)

Die Cramér's-V-Analyse bestätigt die Blockstruktur auf der Ebene der diskreten Klassifikation. Innerhalb der Profitabilitätsschicht ist die Quadrantenübereinstimmung moderat bis stark: ROA $\times$ ROE ($V = 0{,}60$), ROA $\times$ EBIT ($V = 0{,}31$), EBIT $\times$ FCF ($V = 0{,}28$). Cross-kategorial fällt $V$ unter 0,20. Die mechanische ROE $\times$ D/E-Kopplung manifestiert sich auch hier ($V = 0{,}27$), getrieben durch die $\sigma$-Korrelation, die die Quadrantenposition über die Volatilitätsdimension verschiebt.

## 6.3 Zeitliche Manifestation: Event-Analyse

### Identifizierte Peak-Windows

Die datengetriebene Peak-Identifikation ergibt elf Quartale, die das Kriterium ($\geq 3$ Kennzahlen im 90. Perzentil) erfüllen. Diese gruppieren sich in drei Krisencluster.

![Abb. 6.4: Timeline der identifizierten Peak-Windows. Elf Quartale in drei Krisenclustern: Dot-Com (2000Q4–2002Q1), Globale Finanzkrise (2008Q4–2009Q3) und COVID-19 (2020Q1–2020Q4). Die Kreisgröße zeigt die Anzahl gleichzeitig betroffener Kennzahlen.](Kapitel_6_Grafiken/abb_6_5_event_timeline.png)

Das **Dot-Com-Cluster** (2000Q4–2002Q1) umfasst drei Peak-Quartale mit 3 bis 5 betroffenen Kennzahlen — primär Profitabilität. Das **GFC-Cluster** (2008Q4–2009Q3) ist breiter: 2009Q1 zeigt den höchsten Wert mit 6 betroffenen Kennzahlen und einem mittleren Perzentil von 98 %. Das **COVID-Cluster** (2020Q1–2020Q4) ist das ausgedehnteste: Vier konsekutive Quartale im Peak, davon drei mit 6 betroffenen Kennzahlen. Dass die Events rein datengetrieben — ohne Ex-ante-Datierung — identifiziert werden und mit den drei bekannten Wirtschaftskrisen des Zeitraums korrespondieren, validiert die Methode.

Für die vertiefte Analyse werden die jeweils intensivsten Quartale gewählt: Dot-Com 2001Q1 (5 Kennzahlen), GFC 2009Q1 (6 Kennzahlen) und COVID 2020Q2 (6 Kennzahlen, höchstes mittleres Perzentil).

### Quadranten-Reaktionen auf Events

Die zentrale Frage: Reagieren korrektiv-klassifizierte Unternehmen in Stressphasen anders als persistent-klassifizierte? Die Quadrantenklassifikation wurde auf Basis des gesamten 25-Jahres-Zeitraums geschätzt — sie ist also ein statisches Merkmal, dessen prädiktive Kraft für dynamische Situationen geprüft wird.

![Abb. 6.5: Quadranten-Reaktionen in drei Krisenereignissen (ROA). Horizontale Balken zeigen den Median der ROA-Quartalsveränderung (ΔY) pro Quadrant. In allen drei Events differenziert die Quadrantenklassifikation die Reaktionsstärke.](Kapitel_6_Grafiken/abb_6_4_event_reaktionen.png)

**Dot-Com 2001Q1 (ROA):** Die Quadranten differenzieren deutlich. Korrektiv-Stabil ($\Delta Y = +0{,}0004$) und Persistent-Stabil ($\Delta Y = +0{,}0009$) zeigen nahezu keine Reaktion. Korrektiv-Volatil ($-0{,}0004$) und Persistent-Volatil ($-0{,}0010$) zeigen negative Veränderungen — die volatilen Quadranten absorbieren den Schock. Die Vorzeichen-Differenz zwischen stabilen und volatilen Quadranten beträgt den Faktor 2,5.

**GFC 2009Q1 (ROA):** Alle Quadranten zeigen positive Veränderungen (Erholungsphase nach dem Tiefpunkt 2008Q4). Persistent-Volatil ($+0{,}0021$) erholt sich am stärksten — diese Unternehmen hatten den größten Einbruch erlitten und zeigen nun die stärkste absolute Erholung. Korrektiv-Stabil ($+0{,}0004$) reagiert am schwächsten, weil diese Unternehmen kaum eingebrochen waren.

**COVID 2020Q2 (ROA):** Das breiteste Event. Alle Quadranten zeigen starke positive Veränderungen (Rebound nach dem COVID-Einbruch). Persistent-Volatil ($+0{,}0029$) und Korrektiv-Volatil ($+0{,}0029$) dominieren, Korrektiv-Stabil ($+0{,}0011$) reagiert am schwächsten. Die Differenz zwischen den Extremen beträgt den Faktor 2,6.

Das konsistente Muster über alle drei Events: Volatile Quadranten zeigen stärkere absolute Reaktionen — sowohl im Einbruch als auch in der Erholung. Stabile Quadranten dämpfen den Effekt. Die Quadrantenklassifikation, die auf dem gesamten Zeitraum geschätzt wurde, hat also prädiktive Kraft für das Verhalten in konkreten Krisenereignissen. Das ist kein triviales Ergebnis, denn die Klassifikation könnte theoretisch von den Events selbst getrieben sein. Die Tatsache, dass die Events nur drei von 100 Quartalen umfassen und die Klassifikation auf dem gesamten Zeitraum basiert, spricht dagegen.

### Cross-Ratio-Reaktionsmuster

Die Event-Analyse über alle sieben Kennzahlen hinweg zeigt ein zusätzliches Muster: In den COVID-Quartalen reagieren nicht nur die Profitabilitätskennzahlen, sondern auch Kapitalstruktur-Kennzahlen zeigen Ausschläge (Debt-to-Equity-Median bis $-0{,}034$ bei Persistent-Volatil in 2020Q3). Die Finanzkrise und COVID sind also breitere Events als Dot-Com, das primär die Profitabilitätsschicht betraf. Dieses Ergebnis bestätigt die datengetriebene Peak-Identifikation, die 2020Q2 als breitestes Event mit 6 von 7 betroffenen Kennzahlen identifiziert.

## 6.4 Zusammenfassung FF2

FF2 fragte: Wie hängen die Dynamikmuster zusammen, und wie manifestieren sie sich über die Zeit? Die Ergebnisse liefern zwei Hauptbefunde:

Erstens zeigt die querschnittliche Analyse **schichtinterne Kohärenz bei schichtübergreifender Unabhängigkeit**. Die $\varphi_1$-Korrelationen sind innerhalb der Profitabilitätsschicht stark ($\rho = 0{,}50$ bis $0{,}78$), zwischen den Schichten vernachlässigbar ($|\rho| < 0{,}10$). Die $\sigma$-Korrelationen sind stärker vernetzt, enthalten aber mechanische Kopplungen (ROE $\times$ D/E: $\rho_\sigma = 0{,}82$), die von ökonomischen Zusammenhängen getrennt werden müssen. Diese Differenzierung — $\sigma$ als gemeinsamer Faktor, $\varphi_1$ als kennzahlspezifischer Parameter — ist ein zentrales Ergebnis: Die beiden Dimensionen der Quadrantenklassifikation haben unterschiedliche Treiber und sind empirisch weitgehend unabhängig.

Zweitens zeigt die zeitliche Analyse, dass die **statische Quadrantenklassifikation prädiktive Kraft für dynamische Ereignisse** hat. In allen drei identifizierten Krisenclustern (Dot-Com, GFC, COVID) differenziert der Quadrant die Reaktionsstärke: Volatile Quadranten absorbieren Schocks stärker und erholen sich schneller; stabile Quadranten dämpfen den Effekt. Dieses Muster ist konsistent über Events und Kennzahlen.

---

*FF2 hat die Interdependenz der Dynamikmuster und ihre zeitliche Validierung gezeigt. Das folgende Kapitel 7 (FF3) fragt nun: Welche externen Merkmale — Branche und Unternehmensgröße — bestimmen, in welchem Quadranten ein Unternehmen landet?*
