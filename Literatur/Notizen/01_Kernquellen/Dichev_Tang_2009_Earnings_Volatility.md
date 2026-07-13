---
type: literatur
author: "Dichev, Tang"
year: 2009
title: "Earnings volatility and earnings predictability"
journal: "Journal of Accounting and Economics"
tags: 
  - literatur
  - persistenz
  - forschungsfrage1
  - kernquelle
relevanz: 5
status: "🔄 Zu lesen"
forschungsfrage: "[[FF1_Systematische_Unterschiede]]"
---

# Dichev & Tang (2009) - Earnings Volatility and Predictability

**Vollständiger Titel:** Earnings volatility and earnings predictability  
**Autoren:** Ilia D. Dichev, Vicki Wei Tang  
**Jahr:** 2009  
**Journal/Quelle:** Journal of Accounting and Economics, 47(1-2), 160-181  
**DOI/Link:** 10.1016/j.jacceco.2008.09.005  
**Status:** 🔄 Zu lesen

---

## 📌 Relevanz für Masterarbeit

**Warum lesen?**
- **FF1:** Liefert empirische Benchmark-Werte für Persistenz (β = 0.44 bis 0.93)
- **Methodik:** AR(1)-Koeffizient ist konzeptionell äquivalent zu GARCH-Persistenz (α+β)
- **Theorie:** Definiert Stabilität/Volatilität als Qualitätsdimension von Kennzahlen

**Relevanz-Score:** ⭐⭐⭐⭐⭐ (5/5 Sterne)

**Verwendung in:**
- Theoriekapitel: Definition von Persistenz
- Hypothesenableitung: [[Hypothese_H1b]]
- Ergebnisdiskussion: Benchmark-Vergleich meiner α+β-Werte

---

## 🎯 Kernaussage (1 Satz)

Vergangene Earnings-Volatilität reduziert die Persistenz künftiger Earnings systematisch von β = 0.93 (niedrige Vol.) auf β = 0.44 (hohe Vol.), wobei dieser Effekt bis zu 5 Jahre anhält.

---

## 📊 Methodischer Ansatz

**Daten:**
- Stichprobe: 1.000 größte US-Unternehmen
- Zeitraum: 1964-2004 (40 Jahre)
- Quelle: Compustat
- Struktur: Panel (firm-year), annual data

**Methodik:**
- **Persistenz-Modell:** ROA(t+1) = α + β·ROA(t) + ε
- **Volatilitäts-Messung:** 5-Jahres rolling window Standardabweichung des ROA
- **Gruppierung:** Volatilitäts-Quintile
- **Verfahren:** OLS-Regression mit Fixed Effects

**Warum relevant für mich?**
- ✅ Kann ich übernehmen: Volatilitäts-Quintile als Validierung für K-Means-Cluster
- ✅ Benchmark-Werte: Meine GARCH-Persistenz (α+β) sollte zwischen 0.44-0.93 liegen
- ⚠️ Was ich anders mache: GARCH statt AR(1), europäische Daten statt US, ggf. quarterly statt annual

---

## 📝 Zentrale Ergebnisse

### Persistenz nach Volatilitäts-Quintilen

| Quintil | Volatilität | Persistenz β | Half-Life | Interpretation |
|---------|-------------|--------------|-----------|----------------|
| Q1 | Niedrigste | **0.93** | ~9.6 Perioden | Sehr stabil |
| Q2 | Niedrig-Mittel | 0.82 | ~3.5 Perioden | Stabil |
| Q3 | Mittel | 0.71 | ~2.1 Perioden | Moderat |
| Q4 | Mittel-Hoch | 0.59 | ~1.3 Perioden | Volatil |
| Q5 | Höchste | **0.44-0.51** | ~0.7 Perioden | Instabil |

**Differenz Extremgruppen:** 0.42 bis 0.49 Punkte

### Zeitliche Persistenz
- Volatilitäts-Effekt bleibt **bis zu 5 Jahre** signifikant
- Auch mit 5-Jahres-Lag: Vorhersagekraft für aktuelle Persistenz

### Robustheit
- Konsistent über verschiedene Rentabilitäts-Metriken (ROA, ROE, EBIT-Marge)
- Konsistent über Branchen hinweg

---

## 💡 Zitate & Argumente

> "Earnings volatility has a pervasive negative impact on the time-series properties of earnings, particularly earnings persistence." (S. 160)

**Verwendbar für:** Einleitung - Problemstellung, Theoriekapitel

---

> "The persistence of earnings declines monotonically with earnings volatility—from 0.93 for the lowest volatility quintile to 0.44 for the highest volatility quintile." (S. 171)

**Verwendbar für:** Ergebnisdiskussion - Benchmark-Vergleich

---

> "The effect of past volatility on current earnings persistence extends at least five years into the past." (S. 174)

**Verwendbar für:** Diskussion - Implikationen für ARIMA-Prognosen

---

## 🔗 Verbindungen zu anderen Papers

**Vorgänger (zitieren diese Studie):**
- [[Lipe_1990_Earnings_Components]] → Konzept der Earnings Volatility
- [[Sloan_1996_Accruals]] → Accruals und Earnings Persistence

**Nachfolger (bauen darauf auf):**
- [[Lewellen_Resutek_2019_Disaggregation]] → Disaggregation der Persistenz-Komponenten
- [[Francis_2004_Earnings_Attributes]] → Earnings Quality Framework

**Methodisch verwandt:**
- [[Zhu_2025_GARCH_ROA]] → GARCH-Anwendung auf ROA/ROE (direkte Weiterentwicklung)
- [[Pandey_Sinha_2022_Asia_Pacific]] → Persistenz in anderen Regionen

**Ergänzend:**
- [[Nissim_Penman_2001_DuPont]] → DuPont-Zerlegung der Persistenz-Treiber

---

## 🧠 Konzepte & Definitionen

**Earnings Persistence:**
- Definition laut Paper: "Slope-Koeffizient β aus der Regression von ROA(t+1) auf ROA(t)"
- Interpretation: β nahe 1 = hohe Trägheit/Stabilität, β nahe 0 = Mean-Reversion
- Link zu eigener Notiz: [[Konzept_Persistenz_Definition]]

**Earnings Volatility:**
- Definition: 5-Jahres-Standardabweichung des ROA
- Normalisierung: Variationskoeffizient (σ/μ) für Vergleichbarkeit
- Link zu eigener Notiz: [[Konzept_Volatilität_Messung]]

**Äquivalenz zu GARCH:**
- AR(1)-Koeffizient β ≈ GARCH-Persistenz (α+β)
- Beide messen "Trägheit" von Schocks im System
- Link zu eigener Notiz: [[Konzept_GARCH_AR1_Äquivalenz]]

---

## ❓ Offene Fragen / Kritik

### Limitationen des Papers
- ⚠️ **Nur US-Daten:** Gilt der 0.44-0.93 Bereich auch für DAX/europäische Unternehmen?
- ⚠️ **Annual Data:** Wie ändern sich Ergebnisse bei quarterly data (mehr Datenpunkte)?
- ⚠️ **AR(1) vs. GARCH:** Paper nutzt einfaches AR(1), kein Volatility Clustering

### Fragen für meine Arbeit
- [ ] Sind meine GARCH-Persistenzwerte (α+β) im Bereich 0.44-0.93?
- [ ] Wenn nein: Ist das ein IFRS vs. US-GAAP Effekt?
- [ ] Kann ich Volatilitäts-Quintile zur Validierung meiner K-Means-Cluster nutzen?
- [ ] Zeigt sich der 5-Jahres-Lag-Effekt auch in meinen Daten?

---

## ✅ To-Do

- [ ] Paper vollständig gelesen (alle 22 Seiten)
- [ ] Tabelle 3 (Persistenz-Werte) für Benchmark extrahieren
- [ ] Figure 1 (Visualisierung Quintile) für Präsentation adaptieren
- [ ] In [[Theoriekapitel_Persistenz]] integriert
- [ ] Literaturverzeichnis-Eintrag erstellt
- [ ] Zitate in Zotero/Endnote eingepflegt

---

**Tags:** #literatur #persistenz #forschungsfrage1 #kernquelle #arima_äquivalent #benchmark
