from database import create_table
from utils import task_manager

def main():
    create_table()
    task_manager()

  # Erstellen eines User-Objekts mit den gewünschten Attributen
  user1 = User(name="Max Mustermann", age=30, gender="Männlich")

  # Methode zum Erstellen des Users aufrufen
  user1.create_user()

  # Methode zum Löschen eines Users (mit einer spezifischen ID) aufrufen
  # Beispiel: Lösche den Benutzer mit ID 1
  user1.delete_user(1)

main()