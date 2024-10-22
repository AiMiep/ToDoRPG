import sqlite3

# Verbindung zur Datenbank aufbauen
def get_database_cursor():
    database = sqlite3.connect('taskify.db')
    cursor = database.cursor()
    return database, cursor

# Datenbank speichern und schließen
def commit_and_close(database):
    database.commit()
    database.close()

def create_table():
    database, cursor = get_database_cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            age INT,
            gender TEXT
        )
    ''')

    database.execute(''' 
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            status TEXT,
            deadline TEXT
        )
    ''')

    commit_and_close(database)
