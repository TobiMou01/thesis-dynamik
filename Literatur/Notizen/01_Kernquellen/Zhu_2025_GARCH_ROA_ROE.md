---
type: literatur
author: "Zhu, Lyu, Li, Chen"
year: 2025
title: "The wave-particle duality of corporate financial metrics"
journal: "PLOS ONE"
tags: 
  - literatur
  - garch
  - forschungsfrage1
  - kernquelle
  - methodik
relevanz: 5
status: "🔄 Zu lesen"
forschungsfrage: "[[FF1_Systematische_Unterschiede]]"
---

# Zhu et al. (2025) - GARCH auf ROA/ROE

**Vollständiger Titel:** The wave-particle duality of corporate financial metrics: A combined continuous-discrete model  
**Autoren:** Zhu, X., Lyu, Y., Li, Z., Chen, W.  
**Jahr:** 2025  
**Journal/Quelle:** PLOS ONE, 20(11), e0336976  
**DOI/Link:** Open Access PLOS ONE  
**Status:** 🔄 Zu lesen

---

## 📌 Relevanz für Masterarbeit

**Warum lesen?**
- **EINZIGE Studie** die GARCH explizit auf ROE und ROA anwendet
- **Kritische Warnung:** Negative R²-Werte ohne Jump-Komponenten
- **Methodischer Wegweiser:** Zeigt Herausforderungen bei GARCH auf Accounting-Daten

**Relevanz-Score:** ⭐⭐⭐⭐⭐ (5/5 Sterne)

**Verwendung in:**
- Methodikkapitel: Legitimierung GARCH-Anwendung auf Kennzahlen
- Methodikkapitel: Diskussion der Modellgüte (R², Heavy-Tails)
- Limitationen: "Warum meine R²-Werte möglicherweise niedrig sind"

---

## 🎯 Kernaussage (1 Satz)

GARCH-Modelle auf ROA/ROE zeigen ohne Jump-Diffusion-Komponenten negative R²-Werte, aber mit erweitertem Modell (5-Jahres Euclidean Norm) erreichen sie Adjusted R² = 0.430.

---

## 📊 Methodischer Ansatz

**Daten:**
- Stichprobe: 805 börsennotierte chinesische Manufacturing-Unternehmen
- Zeitraum: 2009-2024 (15 Jahre)
- Quelle: CSMAR-Datenbank (China Stock Market & Accounting Research)
- Frequenz: Annual

**Methodik:**
- **GARCH-Basismodell:** σ²(t) = ω + α·ε²(t-1) + β·σ²(t-1)
- **Erweiterung:** Jump-Diffusion nach Merton (1976)
- **Multivariate Version:** 5-Jahres Euclidean Norm als Feature
- **Verteilung:** Student-t statt Normal (Heavy-Tails, df < 2)

**Warum relevant für mich?**
- ✅ **Direkte Referenz:** Wenn Prof. fragt "Hat jemand das schon gemacht?" → JA, diese Studie
- ⚠️ **Warnung:** Rechne mit schlechter Modellanpassung (R² < 0 möglich)
- ✅ **Lösung:** Proxies verwenden wenn GARCH nicht konvergiert, oder Jump-Komponenten
- ⚠️ **Heavy-Tails:** Residuen-Diagnostik ist kritisch

---

## 📝 Zentrale Ergebnisse

### Modellgüte

| Modell | R² | Adjusted R² | Anmerkung |
|--------|-----|-------------|-----------|
| Reines GARCH | **< 0** | n/a | Nicht verwendbar |
| GARCH + Jumps | 0.450 | 0.430 | Akzeptabel |
| Multivariate (5y) | 0.455 | 0.430 | Beste Performance |

### Residuen-Eigenschaften
- **Heavy-Tails:** Student-t Freiheitsgrade < 2
- **Kurtosis:** Extrem hoch (> 10)
- **Normalitätstest:** Stark abgelehnt

### GARCH-Parameter (wenn konvergiert)
- α (ARCH-Term): 0.05 - 0.15
- β (GARCH-Term): 0.60 - 0.80
- **Persistenz α+β:** 0.65 - 0.95
- **Interpretation:** Moderat bis hoch persistent

---

## 💡 Zitate & Argumente

> "The pure GARCH model exhibits negative R² values when applied to accounting ratios, indicating poor model fit without incorporating jump components."

**Verwendbar für:** Methodikkapitel - Rechtfertigung für Proxies oder erweiterte Modelle

---

> "Accounting metrics display extreme heavy-tails with Student-t degrees of freedom consistently below 2, requiring non-normal error distributions."

**Verwendbar für:** Methodikkapitel - Residuen-Diagnostik, Robustheitschecks

---

> "The Euclidean norm over 5-year windows improves model fit substantially, suggesting temporal aggregation reduces noise in accounting data."

**Verwendbar für:** Diskussion - Wenn ich glättende Transformationen verwende

---

## 🔗 Verbindungen zu anderen Papers

**Theoretische Grundlage:**
- Merton (1976) - Jump-Diffusion-Modelle
- Bollerslev (1986) - GARCH-Familie

**Methodisch verwandt:**
- [[Dichev_Tang_2009_Earnings_Volatility]] → Persistenz-Konzept (aber AR(1) statt GARCH)
- [[Engle_1982_ARCH]] → ARCH/GARCH-Originalpaper (auf Aktienrenditen)

**Kontrast:**
- **Aktienrenditen-Literatur:** GARCH funktioniert gut, R² > 0.7
- **Accounting-Kennzahlen:** Problematisch, zusätzliche Modellierung nötig

**Ergänzend:**
- [[Pandey_Sinha_2022_Asia_Pacific]] → Persistenz in Asien (aber ohne GARCH)

---

## 🧠 Konzepte & Definitionen

**Jump-Diffusion:**
- Definition laut Paper: Kombination aus kontinuierlicher GARCH-Volatilität und diskreten Sprüngen (Jumps)
- Notwendig weil: Accounting-Daten haben plötzliche Ereignisse (M&A, Restrukturierung)
- Link zu eigener Notiz: [[Konzept_Jump_Diffusion]]

**Heavy-Tails:**
- Definition: Residuen folgen Student-t mit df < 2 statt Normalverteilung
- Konsequenz: Standardfehler sind unterschätzt, Tests zu liberal
- Link zu eigener Notiz: [[Konzept_Heavy_Tails_Accounting]]

**Euclidean Norm (5-Jahres):**
- Berechnung: √(ROA₁² + ROA₂² + ... + ROA₅²)
- Zweck: Glättung von Ausreißern, robusteres Feature
- Link zu eigener Notiz: [[Konzept_Temporal_Aggregation]]

---

## ❓ Offene Fragen / Kritik

### Limitationen des Papers
- ⚠️ **Nur China:** Manufacturing-Sektor, anderes Rechnungslegungssystem
- ⚠️ **Komplexes Modell:** Jump-Diffusion ist schwer zu implementieren
- ⚠️ **R² immer noch niedrig:** Selbst mit Jumps nur 0.43

### Fragen für meine Arbeit
- [ ] Wenn mein GARCH-Modell negative R² hat → ist das normal/okay?
- [ ] Soll ich Jump-Komponenten integrieren (komplex) oder Proxies verwenden (einfach)?
- [ ] Wie teste ich auf Heavy-Tails in meinen Residuen? (Jarque-Bera-Test?)
- [ ] Ist die 5-Jahres-Norm eine sinnvolle Alternative zu GARCH-Parametern?

### Was ich anders machen würde
- ✅ Quarterly statt Annual Data → mehr Datenpunkte, bessere GARCH-Schätzung
- ✅ Europäische Daten → IFRS statt Chinese GAAP
- ⚠️ Eventuell: GARCH-Parameter als Features nutzen, nicht für Prognosen

---

## ✅ To-Do

- [ ] Paper vollständig gelesen (Fokus: Methodology Section)
- [ ] Appendix: GARCH-Spezifikation im Detail verstehen
- [ ] Code (wenn verfügbar): Implementierung für eigene Daten adaptieren
- [ ] In [[Methodikkapitel_GARCH]] integriert
- [ ] **Kritisch:** Diskussion mit Prof. Stollhoff über Modellanpassung
- [ ] Literaturverzeichnis-Eintrag erstellt

---

**Tags:** #literatur #garch #forschungsfrage1 #kernquelle #methodik #warnung #heavy_tails
