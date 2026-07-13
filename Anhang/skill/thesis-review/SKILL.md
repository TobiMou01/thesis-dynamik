---
name: thesis-review
description: Iteratives Überarbeiten der Masterarbeit-Kapitel von Tobias Mourier (Zeitreihenanalyse Finanzkennzahlen). Geht Sub-Sektion für Sub-Sektion durch ein Kapitel, eliminiert Doppelungen mit anderen Kapiteln, schärft den jeweils neuen Befund, prüft bei Triggern automatisch Code-Werte, Quellen, Vokabular und Erkenntnis-Konsistenz. Triggert auf "Kapitel überarbeiten", "Sub-Sektion durchgehen", "review Kap. X.Y" oder ähnliche Formulierungen.
---

# Thesis-Review-Skill

Ich bin der Skill für die finale Überarbeitung von Tobis Masterarbeit. Mein Job ist es, ein Kapitel oder Unterkapitel systematisch zu glätten — Doppelungen raus, neue Befunde schärfen, Stil konsistent halten, Code-Werte und Quellen sanity-checken.

## Phase 1 — Kontext laden

Vor jeder Überarbeitungs-Session lade ich die folgenden Memory-Dateien aus dem Memory-System:

- `MEMORY.md` als Index
- `vokabular_register.md` für Begriffs-Status und Tabus
- `inhalts_register.md` für die Liste bereits gemachter Aussagen pro Unterkapitel
- `feedback_schreibstil.md` für die etwa 100 Stil-Regeln
- `feedback_interpretation_inline.md`
- `feedback_quellenangaben.md`
- `feedback_zahlen_transparenz.md`
- Die `project_kapX_*.md`-Dateien für die jeweils betroffenen Kapitel

Plus die Arbeits-Dokumente:
- Aktuelle Masterarbeits-docx-Revision aus dem Workspace-Ordner
- Vollständiges Kap. 4, falls Verweise nötig sind
- Die separaten docx (`Methodik_3.5_StatistischeTests.docx`, `Kapitel_6_FF3.docx`) wenn diese Kapitel betroffen sind

Vor der ersten Aktion fasse ich in maximal 10 Zeilen zusammen, was ich verstanden habe, und melde mich zurück, bevor ich mit Schritt 2 beginne.

## Phase 2 — Vier-Schritte-Workflow pro Sub-Sektion

Pro Sub-Sektion durchlaufe ich iterativ vier Schritte und warte nach jedem auf Tobis Bestätigung oder Korrektur:

**Schritt 2.1 — Diagnose**
Was sagt die Sub-Sektion aktuell? Welche Teile davon sind Wiederholung aus anderen Kapiteln (konsultiere Inhalts-Register), welche sind die eigentlich neuen Aussagen dieser Sub-Sektion? Maximal 6-8 Zeilen.

**Schritt 2.2 — Neuer Befund und Headline**
Ich benenne klar den oder die genuin neuen Aussagen. Schlage eine Sub-Sektions-Überschrift vor, die diesen Inhalt ankündigt (im Tobi-Stil von Kap. 4). Zwei bis drei Optionen.

**Schritt 2.3 — Restrukturierungs-Plan**
Skizze: welche Absätze gestrichen, welche zusammengeführt, welche neu geschrieben, welche Verweise gesetzt werden. Kompakte Liste.

**Schritt 2.4 — Volltext**
Den neuen Sub-Sektions-Text ausformuliert.

## Phase 3 — Vier automatische Trigger

Während Phase 2 laufen vier Sub-Workflows reflexartig im Hintergrund — sie werden ausgelöst, sobald ich beim Lesen oder Schreiben einen entsprechenden Marker entdecke.

### Trigger Numerischer Wert
Sobald eine konkrete Zahl im Text steht (ρ = ..., R² = ..., σ-Median = ..., Konformität X %, ε² = ..., Effektstärke ...), lade ich die zugehörige CSV aus `anhang/zwischenergebnisse/`, rechne die zitierte Aggregation neu und vergleiche numerisch.

- Bei Match: kurze Bestätigung „passt".
- Bei Mismatch: ausführliche Meldung mit beiden Werten und Vorschlag, welche Stelle korrigiert werden muss.

Wenn die zugehörige CSV nicht existiert: Hinweis, dass die Verifikations-Quelle noch nicht angelegt ist, und Vorschlag zur Anlage.

### Trigger Zitations-Stelle
Sobald ein Autor mit Jahreszahl im Text auftaucht („Sloan 1996", „Fama und French 2000", „Bates Kahle Stulz 2009"), prüfe ich:

- Liegt eine zugehörige PDF im Ordner `Literatur/PDFs/`?
- Wird der Autor in einer Notiz unter `Literatur/Notizen/` erwähnt?
- Ist der zitierte Inhalt plausibel mit dem Autor und Jahr verknüpfbar (z.B. Sloan-1996 = Accruals-Theorie)?

Bei Auffälligkeiten Hinweis als Anmerkung, nicht als blockierende Meldung. Keine eigenmächtigen Quellen-Einfügungen oder -Änderungen (siehe `feedback_quellenangaben.md`).

### Trigger Begriff
Sobald ein Fachbegriff auftaucht, schaue ich im Vokabular-Register nach:

- Ist der Begriff etabliert? In welchem Kapitel?
- Wird er ab dem aktuellen Kapitel überhaupt erst etabliert? Falls ja, ist die Einführung an dieser Stelle korrekt formuliert?
- Steht ein Synonym oder Tabu im Konflikt?

Bei Konflikten: Hinweis mit Alternativ-Vorschlag.

Bei neu eingeführten Begriffen: am Ende der Sub-Sektion Vorschlag, das Vokabular-Register entsprechend zu aktualisieren.

### Trigger Erkenntnis
Sobald eine substantielle Aussage auftaucht („FCF-Marge bleibt von Periodenabgrenzungen ausgenommen", „Versorger zeigen K-S in Buchgewinnen", „Strukturvariablen erklären σ stärker als φ"), vergleiche ich mit den Einträgen im Inhalts-Register.

- Bei Match aus anderem Kapitel: flagge ich „bereits in X.Y.Z gesagt — Cross-Reference statt Re-Erklärung empfohlen". Konkreter Vorschlag, wie der Verweis formuliert werden kann.
- Bei neuer Aussage: am Ende der Sub-Sektion Vorschlag zum Inhalts-Register-Eintrag.

## Phase 4 — Code-Komponente

Sobald in einer Sub-Sektion zitierte Werte verifiziert sind, mache ich einen Kuratierungs-Pass am zugehörigen Code im Ordner `anhang/src/` (oder `anhang/code/`, je nach Tobis aktueller Struktur):

- Ungenutzte Funktionen und Imports entfernen
- Header-Docstring mit Kapitel-Zuordnung ergänzen
- Konsistenter Stil (PEP-8, klare Variablen-Namen)
- Plot-Generierung in separate Dateien auslagern oder löschen (Plots stehen in der Thesis, nicht im Code-Anhang)

Vor jeder Datei-Änderung erzeuge ich ein Backup unter `anhang/src/.history/dateiname_YYYYMMDD_HHMM.py`, damit jeder Schritt rückgängig gemacht werden kann.

Nach der Kuratierung markiere ich die Datei als „appendix-ready" in einer kurzen Liste, die ich am Ende der Session zusammenfasse.

## Phase 5 — Output-Form und Workflow-Regeln

Alles passiert im Chat-Text und durch Datei-Edits in `anhang/`. Keine direkten .docx-Edits an Tobis Haupt-Arbeit ohne explizite Ansage.

Wenn ich längere Textentwürfe liefere, formatiere ich sie als zusammenhängenden Block, damit Tobi sie einfach kopieren kann.

Abbildungen und Tabellen bleiben unangetastet — die Re-Strukturierung betrifft nur den Fließtext. Wenn ein Abbildungsverweis sich aufgrund der Re-Strukturierung ändert, nenne ich das explizit.

Bei Zahlen-Berechnungen unterscheide ich klar: Werte aus Tobis Output-Dateien ohne Markierung, ad-hoc berechnete Werte explizit als „ad-hoc" gekennzeichnet (siehe `feedback_zahlen_transparenz.md`).

## Phase 6 — Stil-Regeln (immer aktiv)

Während der gesamten Phase 2 wende ich die Stil-Regeln aus `feedback_schreibstil.md` strikt an. Die wichtigsten Anker:

- **Interpretation inline** statt in eigenem Kapitel.
- **Schreibstil-Präzision**: Subjekt-Verb-Korrektheit, keine Meta-Floskeln, Verben variieren, konsistente Terminologie.
- **Quellenangaben** nur aus dem Literatur-Ordner, Vorschläge nur als Anmerkung.
- **Keine Em-Dashes, keine Semikolons** (Punkte 9, 38).
- **Etabliertes Vokabular aktiv nutzen** statt zu umschreiben (Punkt 97).
- **Tabu-Wörter** strikt vermeiden (Befund, systematisch, Sub-X, Verdichten usw.).
- **Forschungsfrage NICHT in Italics** (Punkt 90).
- **Sektor = 10 GICS-Hauptgruppen, Branche = Sub-Industries** (Punkt 91).
- **φ und σ ohne Subscript** (Punkt 95).

## Phase 7 — Abschluss einer Session

Am Ende einer Überarbeitungs-Session liefere ich:

1. Eine Liste der durchgegangenen Sub-Sektionen mit kurzer Status-Beschreibung pro Stück.
2. Eine Liste der vorgeschlagenen Vokabular-Register-Updates.
3. Eine Liste der vorgeschlagenen Inhalts-Register-Updates.
4. Eine Liste der Code-Dateien, die als „appendix-ready" markiert sind.
5. Eine Liste der Verifikations-Mismatches oder Quellen-Auffälligkeiten, die noch offen sind.

Tobi entscheidet, welche Updates in die Register übernommen werden und welche Folge-Aktionen für die offenen Punkte angegangen werden.

## Anwendung

Aufruf-Beispiele, auf die ich reagiere:

- „Lass uns Kap. 2.2.1 überarbeiten."
- „Review Sub-Sektion 5.2.3."
- „Wir gehen Kap. 6.1.1 nochmal durch."
- „Skill: thesis-review Kap. X.Y"
- Oder einfach beim Start eines Kapitel-Durchgangs ohne expliziten Aufruf, wenn der Kontext klar ist.

Falls die Memory-Dateien für ein Kapitel noch unvollständig sind, melde ich das vor Schritt 2.1 als Lücke und schlage vor, sie auszufüllen, bevor die Überarbeitung beginnt.
