from nicegui import ui
import database
import user

def main():
  database.connectDatabase()
  database.createTables()
  user.create_user()
main()