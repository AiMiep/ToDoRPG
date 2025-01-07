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
    if not database or not cursor:
        return

    try:
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                avatar TEXT,
                rasse TEXT DEFAULT 'Bäcker/in',
                klasse TEXT DEFAULT 'Anfänger'
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                difficulty TEXT,
                description TEXT,
                status TEXT DEFAULT 'open',
                date TEXT,
                deadline TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
    except sqlite3.Error as e:
        print(f"Fehler beim Erstellen der Tabellen: {e}")
    finally:
        commit_and_close(database)
