---
type: literatur
author: "Dzuba, Krylov"
year: 2021
title: "Cluster Analysis of Financial Strategies"
journal: "Mathematics (MDPI)"
tags: 
  - literatur
  - clustering
  - forschungsfrage3
  - kernquelle
  - methodik
relevanz: 5
status: "🔄 Zu lesen"
forschungsfrage: "[[FF3_Strukturelle_Faktoren]]"
---

# Dzuba & Krylov (2021) - K-Means auf Finanzkennzahlen

**Vollständiger Titel:** Cluster Analysis of Financial Strategies of Companies  
**Autoren:** Sergey Dzuba, Dmitry Krylov  
**Jahr:** 2021  
**Journal/Quelle:** Mathematics (MDPI), 9(24), 3192  
**DOI/Link:** 10.3390/math9243192 (Open Access)  
**Status:** 🔄 Zu lesen

---

## 📌 Relevanz für Masterarbeit

**Warum lesen?**
- **Vollständiges K-Means-Protokoll** für Finanzkennzahlen
- **Validierungs-Standards:** Silhouette > 0.2, ARI > 0.9
- **Feature-Auswahl:** 6 Indikatoren als Template

**Relevanz-Score:** ⭐⭐⭐⭐⭐ (5/5 Sterne)

**Verwendung in:**
- Methodikkapitel: K-Means-Implementierung Schritt-für-Schritt
- Ergebniskapitel: Cluster-Validierung (Silhouette, ARI)
- Diskussion: Ökonomische Interpretierbarkeit

---

## 🎯 Kernaussage (1 Satz)

K-Means mit z-Score-Normalisierung und Silhouette-Score-Optimierung (k=7, Score 0.221) identifiziert robuste Finanzstrategien-Cluster (ARI=0.947 bei 25% Sample-Reduktion).

---

## 📊 Methodischer Ansatz

**Daten:**
- Stichprobe: 308 Unternehmen aus 7 EU-Ländern
- Zeitraum: 2015-2019 (5 Jahre)
- Quelle: Bloomberg
- Struktur: Cross-sectional (Durchschnittswerte über 5 Jahre)

**Feature-Set (6 Indikatoren):**
1. **EBIT/Sales** (Profitabilität)
2. **ROCE** (Return on Capital Employed)
3. **Leverage** (Debt/(Debt+Equity))
4. **Goodwill Ratio** (Goodwill/Assets)
5. **Financial Assets Ratio** (Fin. Assets/Assets)
6. **Treasury Stock Ratio** (Treasury/Equity)

**Methodik:**
- **Schritt 1:** z-Score Normalisierung (μ=0, σ=1) – ZWINGEND
- **Schritt 2:** Elbow-Methode (k=3 bis k=15)
- **Schritt 3:** Silhouette-Score für optimales k
- **Schritt 4:** Robustheit via Adjusted Rand Index

**Warum relevant für mich?**
- ✅ Kann ich 1:1 übernehmen: Das 4-Schritte-Protokoll
- ✅ Feature-Auswahl: 6 Indikatoren sind ähnlich zu meinen (ROA, ROE, Leverage, ...)
- ✅ Validierung: Silhouette > 0.2 ist akzeptabel (nicht perfekt, aber realitätsnah)

---

## 📝 Zentrale Ergebnisse

### Optimale Clusteranzahl
- **Elbow:** Deutlicher Knick bei k=7
- **Silhouette:** Maximum bei k=7 (Score = **0.221**)
- **Interpretation:** 7 Cluster, moderate Trennung

### Robustheit (ARI bei Sample-Reduktion)
| Sample-Reduktion | ARI | Interpretation |
|------------------|-----|----------------|
| 0% (Full Sample) | 1.000 | Baseline |
| 10% Reduktion | 0.987 | Sehr robust |
| 25% Reduktion | **0.947** | Robust |
| 50% Reduktion | 0.823 | Moderate Stabilität |

**Median ARI bei 25% Reduktion:** 0.947 → **Sehr robuste Cluster**

### Cluster-Charakterisierung (Beispiel)
- **Cluster 1:** High Leverage, Low Profitability ("Distressed")
- **Cluster 2:** Low Leverage, High ROCE ("Conservative")
- **Cluster 3:** High Goodwill, High Fin. Assets ("M&A-Active")

---

## 💡 Zitate & Argumente

> "z-Score normalization is mandatory before K-Means to ensure equal weighting of features with different scales." (S. 5)

**Verwendbar für:** Methodikkapitel - Preprocessing-Schritte

---

> "A Silhouette score above 0.2 indicates acceptable cluster separation for financial data, where perfect separation (>0.5) is rare due to continuous nature of financial metrics." (S. 8)

**Verwendbar für:** Ergebniskapitel - Rechtfertigung für moderate Silhouette-Werte

---

> "Adjusted Rand Index above 0.9 at 25% sample reduction demonstrates structural stability of clusters beyond sampling artifacts." (S. 11)

**Verwendbar für:** Methodikkapitel - Robustheitschecks

---

## 🔗 Verbindungen zu anderen Papers

**Methodisch verwandt:**
- [[Wang_Lee_2008_Financial_Ratios]] → Ähnlicher K-Means-Ansatz
- [[Johnson_1979_Financial_Ratio_Categories]] → Feature-Auswahl (4 Kategorien)

**Clustering-Validierung:**
- [[Rousseeuw_1987_Silhouette]] → Original Silhouette-Score
- [[Hubert_Arabie_1985_ARI]] → Adjusted Rand Index

**Anwendung ähnlich:**
- [[Altman_1968_Z_Score]] → Verwendet Diskriminanzanalyse statt Clustering
- [[Piotroski_2000_F_Score]] → Score-basierte Klassifikation

---

## 🧠 Konzepte & Definitionen

**z-Score Normalisierung:**
- Formel: z = (x - μ) / σ
- Zweck: Alle Features auf μ=0, σ=1 skalieren
- Link zu eigener Notiz: [[Konzept_Z_Score_Normalisierung]]

**Silhouette-Score:**
- Formel: s(i) = (b(i) - a(i)) / max(a(i), b(i))
- a(i): Durchschnittliche Distanz zu Punkten im eigenen Cluster
- b(i): Durchschnittliche Distanz zu Punkten im nächstgelegenen Cluster
- Interpretation: s > 0.5 = gut, s > 0.2 = akzeptabel, s < 0 = falsch zugeordnet
- Link zu eigener Notiz: [[Konzept_Silhouette_Score]]

**Adjusted Rand Index:**
- Bereich: -1 bis 1 (1 = perfekte Übereinstimmung)
- Zweck: Misst Stabilität der Cluster-Zuordnung bei Resampling
- Interpretation: ARI > 0.9 = sehr robust
- Link zu eigener Notiz: [[Konzept_ARI]]

---

## ❓ Offene Fragen / Kritik

### Fragen für meine Arbeit
- [ ] Welche 6-8 Features wähle ich aus? (Persistenz α+β, Volatilität σ², Half-Life, ...)
- [ ] Ist Silhouette > 0.2 ausreichend oder strebe ich > 0.3 an?
- [ ] Welche Sample-Reduktion teste ich? (10%, 25%, 50%?)
- [ ] Wie interpretiere ich Cluster ökonomisch? (DuPont-Zerlegung? Branchen-Verteilung?)

### Limitationen des Papers
- ⚠️ **Nur 5 Jahre:** Durchschnittswerte glätten Dynamik
- ⚠️ **Cross-sectional:** Keine Zeitreihen-Dynamik im Clustering
- ⚠️ **Silhouette 0.221:** Moderate Trennung, nicht perfekt

### Was ich anders machen würde
- ✅ Zeitreihen-Features nutzen (α+β, Half-Life statt nur Mittelwerte)
- ✅ Eventuell: Temporal Clustering (jedes Jahr separates Clustering, dann Transitions analysieren)

---

## ✅ To-Do

- [ ] Paper vollständig gelesen (Fokus: Methodology Section 3)
- [ ] Figure 3 (Silhouette-Diagramm) für Präsentation adaptieren
- [ ] Appendix: R-Code für ARI-Berechnung testen
- [ ] In [[Methodikkapitel_Clustering]] integriert
- [ ] **Kritisch:** Prof. Stollhoff fragen ob Silhouette 0.2 ausreichend ist
- [ ] Literaturverzeichnis-Eintrag erstellt

---

**Tags:** #literatur #clustering #k_means #forschungsfrage3 #kernquelle #methodik #validierung
