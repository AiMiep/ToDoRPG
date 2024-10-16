import sqlite3

def connectDatabase():
    database = sqlite3.connect('taskify.db')
    return database

def createTables():
    database = connectDatabase()

    # Erstellen der Tabelle, falls sie noch nicht existiert
    database.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL
    )
    ''')

    database.execute('''
             CREATE TABLE IF NOT EXISTS tasks (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 description TEXT,
                 status TEXT,
                 deadline DATE
             )
         ''')

    database.commit()
    database.close()