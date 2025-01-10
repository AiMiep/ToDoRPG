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

        # Tabelle für Items
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                path TEXT,
                rasse TEXT,
                level INTEGER
            )
        ''')

        # Tabelle für Benutzer-Items
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS user_items (
                user_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                item_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            )
        ''')

        # Avatare einfügen
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

        # Items einfügen
        cursor.execute('SELECT COUNT(*) FROM items')
        if cursor.fetchone()[0] == 0:
            items = [
                ("Paint", "images/items/painter-paint.jpg", "Maler/in", 1),
                ("Brushes", "images/items/painter-brushes.jpg", "Maler/in", 2),
                ("Sketch Book", "images/items/painter-sketchbook.jpg", "Maler/in", 3),
                ("Sugar and Salt", "images/items/baker-sugerandsalt.jpg", "Bäcker/in", 1),
                ("Oven Mitt", "images/items/baker-oven mitt.jpg", "Bäcker/in", 2),
                ("Mixer", "images/items/baker-mixer.jpg", "Bäcker/in", 3),
                ("Spell Book", "images/items/witch-book.jpg", "Zauberer/in", 1),
                ("Potion", "images/items/witch-potion.jpg", "Zauberer/in", 2),
                ("Wizard Hat", "images/items/witch-hat.jpg", "Zauberer/in", 3),
            ]
            cursor.executemany('INSERT INTO items (name, path, rasse, level) VALUES (?, ?, ?, ?)', items)
            print("Items wurden erfolgreich zur Datenbank hinzugefügt.")
        else:
            print("Items sind bereits in der Datenbank vorhanden.")

    except sqlite3.Error as e:
        print(f"Fehler beim Erstellen der Tabellen: {e}")
    finally:
        commit_and_close(database)

def check_items():
    database, cursor = get_database_cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    print("Verfügbare Items in der Datenbank:")
    for item in items:
        print(f"ID: {item[0]}, Name: {item[1]}, Pfad: {item[2]}, Rasse: {item[3]}, Level: {item[4]}")
    commit_and_close(database)

def check_tables():
    database, cursor = get_database_cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Vorhandene Tabellen in der Datenbank:")
    for table in tables:
        print(table[0])
    commit_and_close(database)

# Beispiel-Aufruf
if __name__ == "__main__":
    create_table()
    check_tables()
    check_items()
