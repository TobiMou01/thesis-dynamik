---
type: literatur
author: "Rufolo, Paientko, Dziergwa"
year: 2025
title: "M&A Impact on DAX 40 Financial Ratios"
journal: "FinTech (MDPI)"
tags: 
  - literatur
  - dax
  - deutscher_kontext
  - kernquelle
relevanz: 4
status: "🔄 Zu lesen"
forschungsfrage: "Alle (Deutscher Kontext)"
---

# Rufolo et al. (2025) - DAX 40 Studie

**Vollständiger Titel:** M&A Impact on Financial Ratios of DAX 40 Companies  
**Autoren:** Rufolo, A., Paientko, T., Dziergwa, K.  
**Jahr:** 2025  
**Journal/Quelle:** FinTech (MDPI), 4(3), 43  
**DOI/Link:** Open Access MDPI  
**Status:** 🔄 Zu lesen

---

## 📌 Relevanz für Masterarbeit

**Warum lesen?**
- **Aktuellste deutsche Studie** zu Finanzkennzahlen-Dynamik
- **DAX 40 als Benchmark** für meine Ergebnisse
- **IFRS-Jahresabschlüsse** als Datengrundlage

**Relevanz-Score:** ⭐⭐⭐⭐ (4/5 Sterne)

**Verwendung in:**
- Diskussion: Vergleich meiner Ergebnisse mit DAX-Benchmark
- Einleitung: "Aktuelle Studien zu deutschen Unternehmen zeigen..."
- Limitationen: M&A-Effekte als Confounder für Kennzahlen-Sprünge

---

## 🎯 Kernaussage (1 Satz)

Profitabilität (ROA, ROE, Operating Margin) und Liquidität (Current, Quick Ratio) sinken 2 Jahre nach M&A-Transaktionen bei DAX 40-Unternehmen signifikant.

---

## 📊 Methodischer Ansatz

**Daten:**
- Stichprobe: 24 DAX 40-Unternehmen
- Zeitraum: 2017-2022 (6 Jahre)
- Quelle: Bloomberg
- Event: M&A-Transaktionen (vor/nach Vergleich)

**Kennzahlen:**
- **Profitabilität:** ROA, ROE, Operating Margin
- **Liquidität:** Current Ratio, Quick Ratio, Cash Ratio
- **Solvenz:** Debt/Equity, Debt/Assets

**Methodik:**
- Paired Sample t-Tests (pre vs. post M&A)
- OLS-Regression mit M&A-Dummy
- Deskriptive Statistik

**Warum relevant für mich?**
- ✅ Zeigt typische Werte-Bereiche für DAX (z.B. ROA 5-10%, D/E 50-80%)
- ⚠️ Warnung: M&A-Events können meine GARCH-Persistenz verzerren (Jumps)
- ✅ IFRS-Daten wie in meiner Arbeit

---

## 📝 Zentrale Ergebnisse

### Profitabilität (2 Jahre nach M&A)
| Kennzahl | Pre-M&A | Post-M&A | Δ | p-value |
|----------|---------|----------|---|---------|
| ROA | 8.5% | 6.2% | **-2.3%** | < 0.05 |
| ROE | 14.2% | 10.8% | **-3.4%** | < 0.01 |
| Op. Margin | 12.1% | 9.7% | **-2.4%** | < 0.05 |

### Liquidität (2 Jahre nach M&A)
| Kennzahl | Pre-M&A | Post-M&A | Δ | p-value |
|----------|---------|----------|---|---------|
| Current Ratio | 1.45 | 1.28 | **-0.17** | < 0.05 |
| Quick Ratio | 1.12 | 0.98 | **-0.14** | < 0.10 |

### Solvenz (nicht signifikant)
- Debt/Equity bleibt stabil bei ~60%
- Debt/Assets bleibt stabil bei ~35%

---

## 💡 Zitate & Argumente

> "DAX 40 companies show deteriorating profitability and liquidity ratios two years post-M&A, suggesting integration costs outweigh synergy benefits in the short term."

**Verwendbar für:** Diskussion - Erklärung für Kennzahlen-Sprünge in meinen Daten

---

> "All data is based on IFRS-compliant annual reports, ensuring comparability across German blue-chip companies."

**Verwendbar für:** Methodikkapitel - Datenqualität, IFRS-Standard

---

## 🔗 Verbindungen zu anderen Papers

**Deutscher Kontext:**
- [[Doukakis_2010_IFRS_Greece]] → IFRS-Effekte auf Persistenz
- [[Gray_2015_EU_Comparison]] → Kulturelle Faktoren trotz IFRS

**M&A-Literatur:**
- [[King_2004_Merger_Performance]] → M&A zerstört oft Wert
- [[Bruner_2002_M&A_Review]] → Meta-Analyse: 60% der M&A scheitern

---

## 🧠 Konzepte & Definitionen

**M&A als Kennzahlen-Schock:**
- Definition: Sprung (Jump) in Zeitreihe durch Akquisition/Fusion
- Relevanz für GARCH: Jump-Komponente nötig (siehe [[Zhu_2025_GARCH_ROA_ROE]])
- Link zu eigener Notiz: [[Konzept_M&A_Events_als_Jump]]

**DAX 40 Benchmark-Werte:**
- ROA: 5-10% (typisch)
- ROE: 10-15% (typisch)
- Debt/Equity: 50-80% (moderat verschuldet)
- Link zu eigener Notiz: [[Konzept_DAX_Benchmarks]]

---

## ❓ Offene Fragen / Kritik

### Fragen für meine Arbeit
- [ ] Wie viele M&A-Events sind in meinem Sample? (Outlier-Detection!)
- [ ] Soll ich M&A-Events explizit kontrollieren? (Dummy-Variable?)
- [ ] Wenn ich Jumps in GARCH sehe → ist es ein M&A-Event? (manuelle Prüfung)

### Limitationen
- ⚠️ Nur 24 Unternehmen (kleines Sample)
- ⚠️ Event-Study-Design (nicht generalisierbar auf alle DAX-Dynamiken)
- ⚠️ Kurzer Zeitraum (2017-2022, inkl. COVID)

---

## ✅ To-Do

- [ ] Paper gelesen
- [ ] Tabelle 2 (Deskriptive Statistik) für Benchmark-Werte extrahieren
- [ ] In [[Diskussion_DAX_Vergleich]] integriert
- [ ] Literaturverzeichnis-Eintrag erstellt

---

**Tags:** #literatur #dax #deutscher_kontext #ifrs #benchmark #m&a
