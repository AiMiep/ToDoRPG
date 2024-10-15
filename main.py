from nicegui import ui
import database

def main():
  database.connectDatabase()
  database.createTables()

main()