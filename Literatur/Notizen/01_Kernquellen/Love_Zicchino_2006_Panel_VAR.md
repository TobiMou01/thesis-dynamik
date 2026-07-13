---
type: literatur
author: "Love, Zicchino"
year: 2006
title: "Financial development and dynamic investment behavior"
journal: "Quarterly Review of Economics and Finance"
tags: 
  - literatur
  - panel_var
  - forschungsfrage2
  - kernquelle
  - methodik
relevanz: 5
status: "🔄 Zu lesen"
forschungsfrage: "[[FF2_Interdependenzen]]"
---

# Love & Zicchino (2006) - Panel VAR Methodik

**Vollständiger Titel:** Financial development and dynamic investment behavior: Evidence from panel VAR  
**Autoren:** Inessa Love, Lea Zicchino  
**Jahr:** 2006  
**Journal/Quelle:** Quarterly Review of Economics and Finance, 46(2), 190-210  
**DOI/Link:** 10.1016/j.qref.2005.11.007  
**Status:** 🔄 Zu lesen

---

## 📌 Relevanz für Masterarbeit

**Warum lesen?**
- **Methodische Referenz:** Standardwerk für Panel-VAR auf Firm-Level-Daten
- **FF2:** Operationalisierung von Interdependenzen via Granger-Kausalität
- **IRF & FEVD:** Impulse-Response und Variance Decomposition Protokoll

**Relevanz-Score:** ⭐⭐⭐⭐⭐ (5/5 Sterne)

**Verwendung in:**
- Methodikkapitel: Panel-VAR-Spezifikation
- Ergebniskapitel: IRF-Interpretation
- Hypothesen: Operationalisierung von H2a, H2b

---

## 🎯 Kernaussage (1 Satz)

Panel-VAR mit orthogonalisierten Impulse-Response-Funktionen ermöglicht es, "fundamentale Faktoren" (Profitabilität) von "finanziellen Faktoren" (Cashflow, Leverage) zu trennen ohne restriktive q-Theorie-Annahmen.

---

## 📊 Methodischer Ansatz

**Daten:**
- Stichprobe: 36 Länder, firm-level panel data
- Zeitraum: 1988-2003
- Quelle: Worldscope
- Struktur: Unbalanced panel, country-specific effects

**Methodik:**
- **Panel-VAR-Spezifikation:** Y(i,t) = Γ₀ + Γ₁Y(i,t-1) + ... + Γ(p)Y(i,t-p) + f(i) + ε(i,t)
- **Orthogonalisierung:** Cholesky decomposition
- **Fixed Effects:** Helmert transformation
- **IRF:** Orthogonalized impulse responses
- **FEVD:** Forecast Error Variance Decomposition

**Warum relevant für mich?**
- ✅ Kann ich übernehmen: IRF zeigt wie Leverage-Schock auf Profitabilität wirkt
- ✅ FEVD: Welcher Anteil der Varianz von ROA wird durch Leverage erklärt?
- ✅ Fixed Effects: Kontrolliert für unbeobachtete Firmen-Heterogenität

---

## 📝 Zentrale Ergebnisse

### Granger-Kausalität
- **Cash Flow → Investment:** Signifikant, positiv
- **Financial Development → Investment Sensitivity:** Moderierender Effekt

### IRF-Interpretation (Beispiel)
- **Horizont t+1:** Stärkster Effekt (0.15-0.25)
- **Horizont t+3:** Klingt ab auf 0.05-0.10
- **Horizont t+5:** Nahe Null (vollständige Absorption)

### FEVD-Interpretation
- **Cash Flow:** Erklärt 40-50% der Investment-Varianz nach 5 Perioden
- **Profitability:** Erklärt 20-30%
- **Leverage:** Erklärt 10-15%

---

## 💡 Zitate & Argumente

> "Panel VAR allows us to relax restrictive assumptions of traditional q-theory models and lets the data speak for itself regarding causal relationships."

**Verwendbar für:** Methodikkapitel - Rechtfertigung für explorative VAR statt strukturelle Modelle

---

> "Orthogonalized IRFs isolate the effect of one shock while holding all other variables constant, enabling cleaner interpretation of interdependencies."

**Verwendbar für:** Methodikkapitel - Erklärung IRF vs. einfache Korrelation

---

## 🔗 Verbindungen zu anderen Papers

**Methodisch aufbauend:**
- [[Holtz-Eakin_1988_Panel_VAR]] → Original Panel-VAR Methodik
- [[Arellano_Bond_1991_GMM]] → GMM für Panel-Daten

**Anwendung ähnlich:**
- [[Dao_2020_Leverage_Profitability]] → Nutzt Panel VAR für Leverage ↔ Profitability
- [[Doorgakant_2022_Capital_Structure]] → Nutzt VAR für Capital Structure ↔ ROE

**Ergänzend:**
- [[Granger_1969_Causality]] → Original Granger-Kausalitätskonzept

---

## 🧠 Konzepte & Definitionen

**Panel VAR:**
- Definition: VAR-System mit Fixed Effects für Panel-Struktur
- Vorteil vs. Time-Series VAR: Nutzt cross-sectional variation
- Link zu eigener Notiz: [[Konzept_Panel_VAR]]

**Orthogonalized IRF:**
- Berechnung: Cholesky decomposition der Varianz-Kovarianz-Matrix
- Interpretation: Isolierter Effekt eines 1-Std-Schocks auf Variable j
- Link zu eigener Notiz: [[Konzept_IRF_Interpretation]]

**FEVD:**
- Berechnung: Varianzanteil nach h Perioden
- Interpretation: "X erklärt Y% der Varianz von Z"
- Link zu eigener Notiz: [[Konzept_FEVD]]

---

## ❓ Offene Fragen / Kritik

### Fragen für meine Arbeit
- [ ] Welche Lag-Ordnung p? (AIC/BIC für Auswahl)
- [ ] Welche Cholesky-Ordnung? (Theoriebasiert: Profitability exogen → Leverage endogen?)
- [ ] Minimum N pro Gruppe? (Paper: mindestens 50 firms pro country)

### Limitationen
- ⚠️ Cholesky-Ordnung ist nicht eindeutig → Robustheitschecks nötig
- ⚠️ Fixed Effects eliminieren zwischen-Firmen-Varianz
- ⚠️ Keine Kointegration (stationary assumption)

---

## ✅ To-Do

- [ ] Paper vollständig gelesen
- [ ] Appendix: Helmert transformation verstehen
- [ ] In [[Methodikkapitel_VAR]] integriert
- [ ] Code-Beispiel: R-Package "panelvar" testen
- [ ] Literaturverzeichnis-Eintrag erstellt

---

**Tags:** #literatur #panel_var #forschungsfrage2 #kernquelle #methodik #irf #fevd
