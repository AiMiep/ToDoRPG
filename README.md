# ToDoRPG

## Projektbeschreibung

ToDoRPG ist eine motivierende Applikation, mit der Nutzer ihre To-Do-Listen auf spielerische Weise verwalten können. Durch das Erledigen von Aufgaben (Quests) sammelt der virtuelle Charakter Erfahrungspunkte und steigt im Level auf. Die Anwendung bietet eine intuitive Benutzeroberfläche, zahlreiche Anpassungsmöglichkeiten und ein Belohnungssystem für erledigte Aufgaben.

---

## Features

### Aufgabenverwaltung (Quests)

- Erstellen, Bearbeiten, Löschen und Erledigen von Aufgaben
- Schwierigkeitsstufen: **Leicht**, **Mittel**, **Schwer**
- Statusverwaltung: **Erstellt**, **In Bearbeitung**, **Beendet**
- Automatische Erfahrungspunkte-Belohnung

### Benutzerverwaltung

- Erstellung eines individuellen Benutzers mit:
  - Name
  - Rasse (z. B. Mario, Zelda, Pokémon-Trainer)
  - Klasse (z. B. Held, Schurke, Bogenschütze)
  - Auswahl eines Avatars
- Level-System mit automatischer Vergabe von Items beim Aufsteigen
- Anzeige des aktuellen Fortschritts (XP, Level, Inventar)

### Persistente Datenspeicherung

- SQLite-Datenbank für die Verwaltung von:
  - Aufgaben
  - Benutzerdaten
  - Items
  - Avatare
- Einfache Erweiterbarkeit durch vorgefertigte Tabellen

### Benutzeroberfläche (GUI)

- Implementiert mit **NiceGUI**
- Dynamische Seiten:
  - Startseite
  - Benutzererstellung
  - Aufgabenübersicht
  - Benutzerübersicht und -funktionen
- Attraktive Hintergründe und Animationen passend zur gewählten Rasse und Klasse

---

## Projektaufteilung

| Anna                             | Ai Mi                                |
|----------------------------------|--------------------------------------|
| **Gesamte Userfunktionen**       | **Gesamte Aufgabenfunktionen**       |
| Backend + Frontend:              | Backend + Frontend:                  |
| - Erstellung                     | - Erstellung                         |
| - Übersicht Userdaten            | - Bearbeitung                        |
| - Userwechsel                    | - Löschung                           |
| - Benutzerübersicht              | - Updaten                            |
| - Belohnungssystem               | - Levelingsystem                     |
| **Zusatz**: ReadMe               | **Zusatz**: Startseite und Hauptmenü |

---

## Entwicklung

### Technologien
- **Python 3.10+**: Hauptprogrammiersprache.
- **NiceGUI**: Für die Erstellung der Benutzeroberfläche.
- **SQLite**: Für die persistente Datenspeicherung.

### Besonderheiten
- **Gruppenprojekt**:
  - Das Projekt wurde von einer Zweiergruppe entwickelt.
  - Zusammenarbeit über ein zentrales Git-Repository.
- **Modularer Aufbau**:
  - Klare Trennung zwischen Logik, Datenbankoperationen und Benutzeroberfläche.
  - Erweiterbarkeit durch gut strukturierte Dateien und Module.

---

## Installation

### Voraussetzungen

- **Python 3.10+**
- Abhängigkeiten:
  - `nicegui`
  - `sqlite3`

