# 📅 Projektplan – Aufgaben-, Meeting- & Fragen-Management-Tool

## 🧭 Gesamtziel
Entwicklung eines lokalen, leichtgewichtigen Tools zur Verwaltung von Aufgaben, Meetings und Fragen, basierend auf YAML-Dateien als Datenbasis und einer einfachen Python-basierten Benutzeroberfläche.  
Fokus auf Übersichtlichkeit, schnelle Erfassung & Bearbeitung sowie einfache Filterung und Verlinkung zwischen Entitäten.

---

## 🟨 Phase 1 – Grundlagen & Datenstruktur
📆 **Dauer**: 1–1,5 Wochen

| Nr. | Aufgabe | Beschreibung | Ergebnis |
|-----|---------|--------------|----------|
| 1.1 | Anforderungen finalisieren | Letzte Anpassungen an Funktionsumfang, YAML-Felder definieren | Abgestimmtes Konzept |
| 1.2 | Datenstruktur entwerfen | YAML-Schema für Aufgaben, Meetings, Fragen festlegen | Beispieldateien |
| 1.3 | Ordnerstruktur anlegen | `data/tasks`, `data/meetings`, `data/questions` | Saubere Basisstruktur |
| 1.4 | Parser & Helper schreiben | Python-Funktionen zum Laden, Validieren, Speichern | Funktionsfähige Parser |
| 1.5 | Git-Repository initialisieren | Versionskontrolle mit Basiskommentaren | Git Repo bereit |

**🎯 Meilenstein 1:** Datenstruktur & Parser sind stabil und können für Phase 2 (UI) verwendet werden.

---

## 🟩 Phase 2 – Dashboard (UI) – Aufgabenmodul
📆 **Dauer**: 2–3 Wochen

- Auswahl UI-Framework (Textual oder NiceGUI)
- Aufgabenübersicht (Filter, Sortierung)
- Formular zum Anlegen & Bearbeiten von Aufgaben
- Archivierungslogik
- Tests mit realen Beispielen

**🎯 Meilenstein 2:** Aufgabenverwaltung funktionsfähig.

---

## 🟦 Phase 3 – Meetings & Fragen + Integration
📆 **Dauer**: 2–3 Wochen

- Meeting-Modul (Infos, Vorbereitung, Aufgaben)
- Fragen-Modul (Personen, Status, Typ)
- Verknüpfungen zwischen Aufgaben ↔ Meetings ↔ Fragen
- Suchfunktion & Archivmechanismus
- UI-Feinschliff

**🎯 Meilenstein 3:** Voll integriertes Tool für Aufgaben, Meetings & Fragen.

---

## ⚪ Phase 4 – Erweiterungen (Optional)
📆 **flexibel**

- Outlook-Integration  
- Exportfunktionen (CSV, Markdown Reports)  
- Automatische Backups  
- Gantt- oder Kanban-Ansicht

---

## ⏱ Zeitrahmen (Schätzung)

| Phase | Inhalt | Dauer |
|-------|--------|-------|
| 🟨 1 | Datenstruktur & Parser | 1–1,5 Wochen |
| 🟩 2 | Dashboard – Aufgaben | 2–3 Wochen |
| 🟦 3 | Meetings & Fragen | 2–3 Wochen |
| ⚪ 4 | Erweiterungen | optional |

---

## 📌 Hinweise
- Das Projekt wird lokal ausgeführt, YAML dient als Datenbasis  
- Änderungen werden via Git versioniert  
- Fokus: Übersichtlichkeit, einfache Pflege, Erweiterbarkeit  
