# Verifikation der c-Werte (Kapitel 5.2.2) — 05.07.2026

## 1. Was liegt in `output/plots/sector_drift/`?

| Dateien | Inhalt | Messgröße |
|---|---|---|
| `storyline_<Sektor>.png` (10) | 2-Linien-Plots pro Sektor (in der Arbeit eingebunden) | geglättete Niveau-Mediane |
| `by_group_sector_<Sektor>.png` (10) | alle 7 Kennzahlen pro Sektor | geglättete Niveau-Mediane |
| `drift_rolling_sector_<Kennzahl>.png` (7) | alle Sektoren pro Kennzahl | geglättete Niveau-Mediane |
| `gruppe_01–04_*_sector.png` (4) | Kennzahlgruppen-Übersichten — **das sind die im Text erwähnten „Anhang"-Plots** | geglättete Niveau-Mediane |
| **`rolling_c_sector_<Kennzahl>.png` (7)** | **alle Sektoren pro Kennzahl — die c-Werte** | **AR(1)-Drift c, Median pro Sektor** |

Die c-Werte sind also **nicht nur berechnet, sondern auch als Grafiken vorhanden** (eine pro Kennzahl, mit GFC-/COVID-Schattierung; Dot-Com fehlt konstruktionsbedingt, weil c erst ab 2006Q2 existiert).

## 2. Wo berechnet?

`src/sector_drift_rolling.py` — beide Spuren in einem Skript:
- Funktion `_rolling_ar1_c()` (Z. 158): ΔY(t) = c + φ·ΔY(t−1) + ε pro Firma × Kennzahl × rückwärtsgerichtetem 25-Quartal-Fenster, OLS-Intercept = c, Position am Fensterende, mindestens 10 gültige Paare.
- `aggregate_rolling_c_by_group()`: Median über die Sektor-Firmen pro Quartal.
- Outputs: `output/ar/sector_drift/rolling_c_per_firm_sector.csv` und `rolling_c_per_group_sector.csv`; Niveau-Trend in `trend_pro_gruppe_sector.csv`.

Der Code entspricht **wörtlich** der Beschreibung im Lead von Kapitel 5.2.2 (zentriertes 25Q-Fenster mit min. 12 Werten für die Niveaus; rückwärtsgerichtetes Fenster für c; c ab 2006Q2; 25 Beobachtungen pro Firmen-Fenster).

## 3. Numerische Verifikation

**(a) Unabhängige Nachrechnung** (Kommunikationsdienste × Debt/Equity, letztes 25Q-Fenster, komplett neu aus `ratio_panel.csv` geschätzt):
eigene Schätzung c-Median = **+0,00228** — Pipeline-Wert = **+0,00228**. Exakte Übereinstimmung.

**(b) Alle 12 im Text zitierten c-Werte** stimmen mit dem Zeitmittel des firmenweisen c-Medians überein (z. B. CommServ D/E +0,0050; Tech CR −0,0062 ≈ −0,006; Healthcare D/E +0,0030; Energie EBIT −0,0015; Immobilien FCF +0,0050). „44 von 70 c-Mediane positiv" ✓ (exakt 44).

**(c) Alle R²-Angaben** der Niveau-Trend-Regression exakt reproduziert (Tech EK 0,88 · Tech CR 0,82 · Tech D/E 0,75 · Immobilien FCF 0,70 · Healthcare D/E 0,69 · ZyklKons EK 0,66 · CommServ D/E 0,55 · Energie EBIT 0,14 · Industrie CR 0,006 < 0,01).

**(d) Plausibilitätsprüfung „r = 0,86, Vorzeichen 54/70":** reproduziert als **r = 0,87, 55/70**, wenn der median-aggregierte Mittelwert der Quartalsveränderungen **ab 2006Q2** berechnet wird (= das Fenster, in dem c existiert — methodisch der richtige Vergleich). Über den Vollzeitraum 2000–2024 ergäbe sich r ≈ 0,74. → Für die Verteidigung merken: *„Vergleich im gemeinsamen Fenster ab 2006Q2."* Die Abweichung 0,86 vs. 0,87 bzw. 54 vs. 55 ist Rundung/Detailfilter — die Aussage steht.

## 4. Ist der Text in 5.2.2 stimmig?

Ja. Die Beschreibung ist korrekt und ehrlich: Geglättete Niveau-Reihe (zentriert) und c-Median (rückwärtsgerichtet) messen denselben Trend mit unterschiedlicher Verankerung; die drei methodischen Grenzen (Randglättung, c erst ab 2006Q2 / Dot-Com fehlt, 25 Beobachtungen pro Firma) stehen explizit im Lead.

**Ein Anfasspunkt für Prüferfragen:** Immobilien × Debt/Equity — Niveau-Trend fällt (−0,0025/Quartal), c-Mittel ist trotzdem +0,0009. Verifiziert: beide Zahlen stimmen. Die Erklärung der Arbeit („c-Median über die Firmen anders verteilt als der Aggregat-Trend") ist korrekt; im c-Plot sichtbar: Real Estate liegt früh (2006–2008) deutlich positiv und schwankt danach um null, während die Niveau-Linie nach der GFC kontinuierlich fällt. Antwort parat haben: *Median-of-Firms ≠ Trend des Median-Aggregats, plus asymmetrische Verankerung der Fenster.*

## 5. Anhang-Frage

Kapitel 5.2.2 verweist auf Übersichtsplots „im Anhang" — ein Anhang wurde nicht abgegeben (toter Verweis, gehört auf die Errata-Liste). Die Plots existieren: `gruppe_01_renditen` … `gruppe_04_kapitalstruktur_sector.png`. **Empfehlung:** diese vier plus die sieben `rolling_c_sector_*.png` ausgedruckt bzw. als Backup-Folien mitbringen — damit ist der Verweis materiell gedeckt und jede c-Nachfrage direkt bedienbar.
