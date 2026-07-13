# Folienplan zur Fertigstellung — Kolloquium v2 (Stand 05.07., 27 Folien)

## 0. Vorab: Der Grafik-„Widerspruch" bei den Quadranten-Krisen — aufgelöst

**Beide Bilder sind richtig — sie zeigen verschiedene Größen.**

| | Alte Abb. 29 (Arbeit) | Neue Boxplot-Grafik |
|---|---|---|
| Messgröße | **vorzeichenbehaftetes** Median-ΔY je Quadrant, gemittelt über die 4 Profitabilitätskennzahlen | **Betrag** \|ΔY\| pro Firma × Kennzahl (Verteilung) |
| Aussage | *Richtung*: Gibt es eine gerichtete Niveau-Verschiebung? | *Stärke*: Wie groß ist der Ausschlag — egal wohin? |
| Achse | linear, 0 in der Mitte, je Panel andere Grenzen | log, fixe Grenzen über alle drei Krisen |

Die Balken der alten Grafik habe ich aus `window_descriptions.csv` exakt reproduziert (z. B. GFC P-V +0,019; Dot-Com alle nahe 0). In Dot-Com heben sich positive und negative Firmenbewegungen auf → Balken ≈ 0, aber die weiten Fehlerbalken der volatilen Quadranten zeigten schon damals: Die *Streuung* war groß. Das Erzeuger-Skript (04.03.2026) existiert nicht mehr im Repo — die exakte Fehlerbalken-Definition ist nicht mehr rekonstruierbar. **Wichtig:** Die Tests in Kapitel 5.2.3 (Mann-Whitney, r_rb) laufen auf **\|ΔY\|** — die neue Boxplot-Grafik illustriert also genau das, was die Arbeit testet und behauptet („volatil reagiert stärker"). Die alte zeigt etwas, das die Arbeit gar nicht testet.

**Zu „Tech besonders volatil in Dot-Com":** bestätigt — in `g3b_dotcom_tech_markiert.png` sitzen die Tech-Punkte in *jedem* Quadranten am oberen Rand. Genau deshalb trennen die Quadranten in Dot-Com nicht (Tests n.s.): Die Krise war sektoral konzentriert, nicht quadranten-spezifisch. Das ist die Kernaussage der Arbeit — kein Widerspruch.

**Empfehlung:** Im Vortrag nur die neue Boxplot-Grafik zeigen. Falls ein Prüfer Abb. 29 aus der Arbeit anspricht: „Abbildung 29 zeigt die gerichtete Verschiebung — die ist nahe null; getestet und hier gezeigt wird die Reaktionsstärke |ΔY|." Ein souveräner Satz, Thema erledigt.

---

## 1. Pro-Folie-Plan

**Legende:** ✅ fertig lassen · ✏️ ändern · 🗑 löschen · Überschriften-Vorschläge in »…«

| # | Folie | Aktion |
|---|---|---|
| 1–10 | Titel bis Quadranten | ✅ Laut dir fertig. Einzige Sammelaufgabe: Seitenzahlen (siehe Abschluss-Pass). |
| 11 | Volatilität der Kennzahlen | ✏️ **Schnell-Durchlauf-Folie (~25 Sek.).** Die zwei Karten auf je EINE Zeile eindampfen: Karte 1 »σ ist nennergetrieben — Median 0,017 (ROA) bis 0,32 (CR)«, Karte 2 »Vergleich nur innerhalb der Kennzahl → Median-Split je Kennzahl«. Der zweite Punkt ist die Überleitung zur Quadranten-Logik — mehr braucht die Folie nicht, alles Weitere in den Redetext. Überschrift kurz: »Volatilität: nennergetrieben«. |
| 12+13 | Mean Reversion (Build) | ✏️ Gut kompakt. Vier Präzisierungen: (a) Kapitalstruktur-Wert **„−0,07" → „−0,04 … −0,09"** (Arbeit nennt beide Mediane; ein gemittelter Einzelwert ist angreifbar). (b) Folie 13: **Titel fehlt** — beim Build stehen lassen (Morph). (c) Leiste: **„≈ 25 %" → „19–32 %"** (D/E 32,4 · EK 18,6 — präzise statt gemittelt). (d) Doppel-Leerzeichen „Anteil  Mean-Reversion". Und: Die **Robustheits-Zeile ist aus dem Deck gefallen** („4 Spezifikationen · 4 Schwellen · 4 Zeitfenster") — Kernbotschaft 1 aus dem Verteidigungsplan! Als Fußzeile auf 13 wieder rein. |
| 14 | Sektor-Folie | ✏️ **Neubau rechts, Grafik bleibt.** Statt drei Textkarten + drei Chips: eine **Spannweiten-Zeile** mit drei großen Zahlen im Gruppen-Farbcode — »0,12« (Profitabilität) · »0,24« (Liquidität) · »0,13« (Kapitalstruktur), Unterzeile „φ-Spannweite der zehn Sektor-Mediane". Darunter EINE Ausnahmen-Zeile: „Ausnahmen nur, wo externe Mechanik eingreift: Immobilien (REIT-Refinanzierung) · Versorger (Regulierung)". Die drei Profil-Chips: farbige Labels raus (Farben tragen dort keine Aussage) → als Build 2 in neutralem Sage ODER komplett in den Redetext. Überschrift: »Kennzahl schlägt Sektor«. |
| 15 | Konstruktion & Korrekturmechanismus | ✅ Passt. Zwei optionale Ergänzungen für den FF1-Abschluss: Kernsatz als Abbinder-Zeile unten (»Der Markt korrigiert — das Management entscheidet«) — das schließt FF1 hörbar ab. Inhaltlich ist FF1 damit komplett (4.1 ✓ 4.2 ✓ 4.3 ✓); was fehlt, ist nur die Robustheit (→ Folie 13). |
| 16 | φ-Matrix | ✏️ Bild größer ziehen (die Karte hat viel Leerraum), Bildunterschrift auf eine Zeile. Karten rechts ok. Überschrift kurz genug. |
| 17 | σ-Matrix | ✏️ **Rechte untere Karte ist LEER** → dort gehört der Kernsatz hin: »Schocks treffen gemeinsam — korrigiert wird kennzahlspezifisch« (die wichtigste Zeile von FF2!). Links steht „Kopplung nur innerhalb der Profitabilität" — als φ/σ-Gegenüberstellung perfekt. **Entscheidung nötig:** φ×σ (H4, Dichev/Tang) und Lead-Lag sind aus dem Deck gefallen — Empfehlung: NICHT zurück auf die Folie; H4 in den Redetext zu Folie 17 (ein Satz, stützt den Median-Split), Lead-Lag nur als Frage-Antwort/Backup. |
| 18 | Drift (Titel ist Platzhalter) | ✏️ **Allgemeinere Grafik statt Tech-Beispiel — deine Vorarbeit existiert:** `output/ar/aggregat_drift_pro_kennzahl.png` (alle 7 Kennzahlen, Aggregat — die allgemeinste Sicht) oder `gruppe_04_kapitalstruktur_sector.png` (D/E + EK-Quote über alle Sektoren — zeigt die Verschuldungsexpansion direkt). Empfehlung: **aggregat_drift** als Folienbild, aktueller c-Plot (D/E) + Tech-Story ins Backup. Rechte Karten: Tech-Karte raus, stattdessen die Vorzeichen-Bilanz prominent (44/70 · D/E 10/10 · EK 7/10 negativ). Überschrift: »Die Verschuldung driftet — überall«. |
| 19 | Krisen-Boxplots | ✏️ Grafik + Klärung oben. Aber: **Kapitel 5.2.1 (Krisen-Identifikation) fehlt jetzt komplett im Deck.** Dein Briefing wollte es „in einer Grafik, nacheinander eingeblendet" — Vorschlag: Build 1 = Volatilitäts-Timeline breit (»Die Daten datieren die Krisen«), Build 2 = Timeline schrumpft zur Kopfleiste, Boxplots erscheinen darunter. Alternativ minimal: Kriterium nur im Redetext (1 Satz), Timeline ins Backup. Außerdem ist die Folie aktuell sehr voll (Grafik + 3 Karten + 4 Chips + Fußzeile): Chips als eigenen Build ODER die 4 Chips ins Backup und nur die Fußzeile behalten. |
| 20 | „Fünf Strukturvariablen, 98 Tests…" | 🗑 **Löschen.** Alte Version, kein Bild, Inhalte vollständig auf 22+23. |
| 21 | „Der Sektor erklärt…" (ohne Bild) | 🗑 **Löschen.** Alte Version, Inhalte vollständig auf 24. |
| 22 | Testprogramm | ✅ Behalten (dein „nicht mit der Tür ins Haus"-Einstieg). |
| 23 | 6.1 Heatmap | ✏️ **Bild tauschen:** aktuell noch die dunkle Version → `grafiken/g1_ff3_bivariat_heatmap.png` (weiß, ohne Sterne). Überschrift kürzen: »Unternehmensmerkmale wirken auf σ«. |
| 24 | 6.2 Sektoreffekt | ✏️ **Bild tauschen** → `grafiken/g2_ff3_sektor_epsilon.png` (weiß, blau=σ/grau=φ). Überschrift kürzen: »Sektoreffekt: σ ja, φ kaum« — vermeidet die Dopplung mit dem 6.3-Titel. |
| 25 | „Struktur erklärt σ — nicht φ" | ✅ Kernfolie, bleibt. (Später optional: ΔR²-Build, wenn die G3-Rechnung gemacht ist.) |
| 26 | Validierung „(Fazit)" | ✏️ **Umwidmen zur Fazit-Folie** — ihre Inhalte (Cluster 66/65/60/43, FinSrv 29×) stehen jetzt auf Folie 24, doppelt zeigen wäre ein Fehler. Und die Fazit-Folie fehlt noch! Konzept: Die drei FF-Karten von Folie 3 kehren per Morph zurück, jede mit einer Antwortzeile; darunter eine schmale Ausblick-Zeile + Dank. Redetext dafür liegt im Manuskript (Folie 16). |
| 27 | Limitationen | ✅ Bleibt. Einmal auf den alten „AUSBLCK"-Tippfehler prüfen, falls die Zeile noch existiert. |

## 2. Abschluss-Pass (mache ich automatisiert, sobald der Folienbestand steht)

1. **Seitenzahlen vereinheitlichen** — aktuell gemischt („06/13", „07/15", „10/13"). Ein Durchlauf, logische Zählung, korrektes Total.
2. **Überschriften-Pass** — alle Titel auf kurz und knackig (Vorschläge oben in »…«).
3. **Notizen-Abgleich** — Redetexte an die finale Folienstruktur anpassen (der große Text-Pass danach ist ein eigener Schritt).

## 3. Empfohlene Reihenfolge der Umsetzung

1. Du entscheidest die drei offenen Punkte: (a) Folie 19 mit oder ohne Timeline-Build, (b) Folie 18 aggregat_drift oder gruppe_04, (c) Profile auf 14 als Build oder nur Redetext.
2. Ich setze um: 20+21 löschen, 26 zur Fazit-Folie umbauen, Bilder auf 23/24 tauschen, Folie-14-Neubau, Kleinfixes (12/13/17), Timeline-Build falls gewünscht.
3. Abschluss-Pass (Nummerierung + Überschriften).
4. Danach: der große Text-Pass (Professionalisierung des Sprechtexts, angepasst an die finalen Folien).
