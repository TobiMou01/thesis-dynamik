# 📚 MOC: Literatur-Übersicht

> **23 akademische Quellen für die Masterarbeit**  
> Zuletzt aktualisiert: 2025-01-14

---

## 🌟 Top-5 Kernquellen

| Quelle | Relevanz | FF | Warum wichtig? |
|--------|----------|----|-----------------| 
| [[Dichev_Tang_2009_Earnings_Volatility]] | ⭐⭐⭐⭐⭐ | FF1 | Persistenz-Benchmark (β: 0.44-0.93) |
| [[Zhu_2025_GARCH_ROA_ROE]] | ⭐⭐⭐⭐⭐ | FF1 | EINZIGE Studie mit GARCH auf ROA/ROE |
| [[Love_Zicchino_2006_Panel_VAR]] | ⭐⭐⭐⭐⭐ | FF2 | Panel-VAR Methodik (IRF, FEVD) |
| [[Dzuba_Krylov_2021_Cluster_Analysis]] | ⭐⭐⭐⭐⭐ | FF3 | K-Means Validierungs-Protokoll |
| [[Rufolo_2025_DAX_40_M&A]] | ⭐⭐⭐⭐ | DAX | Aktuellste DAX-Studie, IFRS-Benchmarks |

---

## 📑 Nach Forschungsfrage

### FF1: Systematische Unterschiede in zeitlicher Dynamik

**Kernquellen:**
- [[Dichev_Tang_2009_Earnings_Volatility]] - Persistenz β = 0.44-0.93
- [[Zhu_2025_GARCH_ROA_ROE]] - GARCH auf Accounting-Ratios

**Ergänzend:**
- [[Lewellen_Resutek_2019]] - Heterogenitätstests (F-Test)
- [[Pandey_Sinha_2022]] - Größeneffekt (β=0.278)
- [[Canina_Potter_2019_Diversification]] - Diversifikations-Effekt

---

### FF2: Interdependenzen zwischen Kennzahlen

**Kernquellen:**
- [[Love_Zicchino_2006_Panel_VAR]] - Panel-VAR Methodik
- [[Dao_2020_Leverage]] - Leverage ↔ Profitability (bidirektional negativ)
- [[Nissim_Penman_2001_DuPont]] - DuPont-Zerlegung

**Ergänzend:**
- [[Doorgakant_2022_Mauritius]] - Capital Structure ↔ ROE (positiv)
- [[Nyamekye_2024_Ghana]] - Leverage → Firm Value (unidirektional)

---

### FF3: Strukturelle Merkmale & Clustering

**Kernquellen:**
- [[Dzuba_Krylov_2021_Cluster_Analysis]] - K-Means Validierung
- [[Pandey_Sinha_2022]] - Größeneffekt

**Ergänzend:**
- [[Al_Shari_2023_Capital_Intensity]] - Kapitalintensität
- [[Wang_Lee_2008_Financial_Ratios]] - Feature-Selektion
- [[MDPI_2025_DJIA_Sectors]] - Brancheneffekte

---

### Deutscher/EU-Kontext

- [[Rufolo_2025_DAX_40_M&A]] - DAX 40 Benchmark-Werte
- [[Doukakis_2010_IFRS]] - IFRS verbessert NICHT Persistenz
- [[Gray_2015_EU_Cultural]] - Kulturelle Faktoren trotz IFRS

---

### Methodische Grundlagen

**GARCH:**
- [[NYU_V_Lab_GARCH]] - α+β Interpretation, Half-Life
- [[Bollerslev_1986_GARCH]] - GARCH-Original

**Tests:**
- [[Mummolo_Peterson_2018_Heterogeneity]] - Panel-Tests (Hausman, F-Test)
- [[Johnson_1979_Financial_Ratios]] - 4 Kennzahlen-Kategorien

**Theorie:**
- [[Francis_2004_Earnings_Attributes]] - Earnings Quality Framework
- [[Lipe_1990_Earnings_Components]] - Earnings Volatility
- [[Sloan_1996_Accruals]] - Accruals & Persistenz

---

## 📊 Benchmark-Werte aus Literatur

### Persistenz (AR(1) oder GARCH α+β)

| Studie | Wert | Sample | Interpretation |
|--------|------|--------|----------------|
| Dichev & Tang (2009) | 0.44 - 0.93 | 1.000 US, 40y | Volatilität reduziert Persistenz |
| Pandey & Sinha (2022) | 0.278 | 12.001 Asia-Pacific | Moderate Persistenz |
| Lewellen & Resutek (2019) | 0.82 → 0.35 | US, 45y | Decay über 7 Perioden |

### GARCH-Modellanpassung

| Studie | R² | Anmerkung |
|--------|----|-----------|
| Zhu et al. (2025) | < 0 | Reines GARCH unbrauchbar |
| Zhu et al. (2025) | 0.430 | Mit Jump-Komponenten akzeptabel |

### Clustering-Validierung

- **Silhouette:** 0.221 bei k=7 (Dzuba & Krylov 2021) → akzeptabel
- **ARI:** 0.947 bei 25% Reduktion → sehr robust

### DAX-Benchmark (Rufolo 2025)

- **ROA:** 5-10% typisch
- **ROE:** 10-15% typisch
- **Debt/Equity:** 50-80%

---

## 🗂️ Nach Thema

### GARCH-Methodik
- [[Zhu_2025_GARCH_ROA_ROE]]
- [[NYU_V_Lab_GARCH]]
- [[Bollerslev_1986_GARCH]]

### VAR & Kausalität
- [[Love_Zicchino_2006_Panel_VAR]]
- [[Dao_2020_Leverage]]
- [[Doorgakant_2022_Mauritius]]

### Clustering
- [[Dzuba_Krylov_2021_Cluster_Analysis]]
- [[Wang_Lee_2008_Financial_Ratios]]
- [[Johnson_1979_Financial_Ratios]]

### Persistenz
- [[Dichev_Tang_2009_Earnings_Volatility]]
- [[Lewellen_Resutek_2019]]
- [[Pandey_Sinha_2022]]

---

## 📈 Verwendungsmatrix

| Kapitel | Kernquellen | Zweck |
|---------|-------------|-------|
| **Einleitung** | Dichev & Tang (2009), Rufolo (2025) | Problemstellung, DAX-Relevanz |
| **Theorie: Persistenz** | Dichev & Tang (2009), Francis (2004) | Stabilität als Qualitätsdimension |
| **Theorie: DuPont** | Nissim & Penman (2001) | Kennzahlen-Interdependenzen |
| **Methodik: GARCH** | Zhu (2025), NYU V-Lab | α+β-Interpretation, R²-Warnung |
| **Methodik: VAR** | Love & Zicchino (2006), Dao (2020) | Panel VAR, Granger-Kausalität |
| **Methodik: Clustering** | Dzuba & Krylov (2021) | K-Means Validierung |
| **Hypothesen** | Lewellen & Resutek (2019), Mummolo & Peterson (2018) | F-Test, Heterogenität |
| **Ergebnisse** | Alle empirischen Studien | Benchmark-Vergleiche |
| **Diskussion: Faktoren** | Pandey & Sinha (2022), Al-Shari (2023) | Größe, Kapitalintensität |

---

## 🗓️ Leseplan (3 Wochen)

### Woche 1: Kernquellen
- [ ] [[Dichev_Tang_2009_Earnings_Volatility]]
- [ ] [[Zhu_2025_GARCH_ROA_ROE]]
- [ ] [[Dzuba_Krylov_2021_Cluster_Analysis]]

### Woche 2: VAR & Kontext
- [ ] [[Love_Zicchino_2006_Panel_VAR]]
- [ ] [[Dao_2020_Leverage]]
- [ ] [[Rufolo_2025_DAX_40_M&A]]

### Woche 3: Ergänzungen
- [ ] [[Lewellen_Resutek_2019]]
- [ ] [[Nissim_Penman_2001_DuPont]]
- [ ] [[Mummolo_Peterson_2018_Heterogeneity]]

### Bei Bedarf: Restliche 14 Quellen

---

## 🔍 Schnellsuche nach Tags

**Methodik:**
- `tag:#garch` → GARCH-Quellen
- `tag:#panel_var` → VAR-Methodik
- `tag:#clustering` → K-Means

**Forschungsfrage:**
- `tag:#forschungsfrage1` → FF1-relevante Quellen
- `tag:#forschungsfrage2` → FF2-relevante Quellen
- `tag:#forschungsfrage3` → FF3-relevante Quellen

**Kontext:**
- `tag:#deutscher_kontext` → DAX, IFRS, EU
- `tag:#dax` → DAX 40-Studien

---

## ✅ Status-Tracking

**Legende:**
- 🔄 Zu lesen
- 📖 Gelesen
- ✅ Integriert

**Stand:**
- Gelesen: 0/23
- Integriert: 0/23

→ Status ändern in den einzelnen Literatur-Notes

---

## 🔗 Navigation

**Zurück zu:**
- [[00-Start/MOCs/MOC_Gesamtübersicht]] → Hauptübersicht
- [[00-Start/MOCs/MOC_Methodik]] → Methodische Tools
- [[02-Forschung/RQ_Hauptfrage]] → Forschungsfragen

**Siehe auch:**
- [[Paper_Template]] → Template für neue Quellen

---

**Alle 23 Quellen in thematischen Unterordnern verfügbar!**
