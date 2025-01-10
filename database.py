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
        # Tabelle für Avatare
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS avatars (
                avatar_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                path TEXT
            )
        ''')

        # Tabelle für Benutzer
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                rasse TEXT DEFAULT 'Bäcker/in',
                klasse TEXT DEFAULT 'Anfänger',
                avatar_id INTEGER,
                FOREIGN KEY (avatar_id) REFERENCES avatars(avatar_id)
            )
        ''')

        # Tabelle für Aufgaben
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

        # Avatare einfügen, falls sie noch nicht existieren
        cursor.execute('SELECT COUNT(*) FROM avatars')
        if cursor.fetchone()[0] == 0:
            avatars = [
                ("Bäcker/in", "images/avatars/baker.png"),
                ("Maler/in", "images/avatars/painter.png"),
                ("Zauberer/in", "images/avatars/witch.png"),
            ]
            cursor.executemany('INSERT INTO avatars (name, path) VALUES (?, ?)', avatars)
            print("Avatare wurden erfolgreich zur Datenbank hinzugefügt.")
        else:
            print("Avatare sind bereits in der Datenbank vorhanden.")


    except sqlite3.Error as e:
        print(f"Fehler beim Erstellen der Tabellen: {e}")
    finally:
        commit_and_close(database)
