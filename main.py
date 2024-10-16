from nicegui import ui
import database
import user

def main():
  database.connectDatabase()
  database.createTables()
  user1 = user.User(name="Max Mustermann", age=30, gender="Männlich")

  # User anlegen
  user1.create_user()

  # User löschen (Beispiel: User mit ID 1 löschen)
  #user1.delete_user(2)

main()