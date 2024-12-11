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
            users_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
    ''')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            difficulty TEXT,
            description TEXT,
            status TEXT,
            date TEXT,
            deadline TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(users_id)
        )
    ''')

    commit_and_close(database)
