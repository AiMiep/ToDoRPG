from nicegui import ui
import database # Importiert die Funktionen aus database.py
from user import User # Improtiert die User Klasse aus der user.py

def main():
  # Datenbankverbindung und Tabelleninitialisierung
  database.connectDatabase()
  database.createTables()

  # Erstellen eines User-Objekts mit den gewünschten Attributen
  user1 = User(name="Max Mustermann", age=30, gender="Männlich")

  # Methode zum Erstellen des Users aufrufen
  user1.create_user()

  # Methode zum Löschen eines Users (mit einer spezifischen ID) aufrufen
  # Beispiel: Lösche den Benutzer mit ID 1
  user1.delete_user(1)

if __name__ == "__main__":
  main()