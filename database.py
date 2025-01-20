import sqlite3


def get_database_cursor():
    """
    Erstellt eine Verbindung zur SQLite-Datenbank und gibt die Verbindung und den Cursor zurück.
    """
    database = sqlite3.connect('taskify.db')
    cursor = database.cursor()
    return database, cursor


def commit_and_close(database):
    """
    Speichert Änderungen in der Datenbank und schließt die Verbindung.
    """
    database.commit()
    database.close()


def create_table():
    """
    Erstellt alle erforderlichen Tabellen in der Datenbank, falls diese nicht existieren.
    Fügt bei Bedarf neue Spalten hinzu.
    """
    database, cursor = get_database_cursor()

    # Tabelle für Avatare
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avatars (
            avatar_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            path TEXT
        )
    ''')

    # **Prüfen, ob die Spalte "description" in der Tabelle "avatars" fehlt und ggf. hinzufügen**
    cursor.execute("PRAGMA table_info(avatars)")
    columns = [column[1] for column in cursor.fetchall()]
    if "description" not in columns:
        cursor.execute("ALTER TABLE avatars ADD COLUMN description TEXT DEFAULT 'Keine Beschreibung'")
        print("Spalte 'description' zur Tabelle 'avatars' hinzugefügt.")

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
            FOREIGN KEY (avatar_id) REFERENCES avatars (avatar_id)
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
            FOREIGN KEY (user_id) REFERENCES users (user_id)
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
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (item_id) REFERENCES items (item_id)
        )
    ''')


    # Avatare einfügen
    cursor.execute('SELECT COUNT(*) FROM avatars')
    if cursor.fetchone()[0] == 0:  # Wenn keine Avatare existieren
        avatars = [
            ("Bäcker/in", "avatars/baker.png"),  # Nur 'avatars/' ohne 'images/'
            ("Maler/in", "avatars/painter.png"),
            ("Zauberer/in", "avatars/witch.png"),
        ]
        cursor.executemany('INSERT INTO avatars (name, path) VALUES (?, ?)', avatars)
        print("Avatare wurden erfolgreich zur Datenbank hinzugefügt.")

    # Items einfügen
    cursor.execute('SELECT COUNT(*) FROM items')
    if cursor.fetchone()[0] == 0:  # Wenn keine Items existieren
        items = [
            ("Paint", "items/painter-paint.jpg", "Maler/in", 1),
            ("Brushes", "items/painter-brushes.jpg", "Maler/in", 2),
            ("SketchBook", "items/painter-sketchbook.jpg", "Maler/in", 3),
            ("Sugar and Salt", "items/baker-sugerandsalt.jpg", "Bäcker/in", 1),
            ("Oven Mitt", "items/baker-oven mitt.jpg", "Bäcker/in", 2),
            ("Mixer", "items/baker-mixer.jpg", "Bäcker/in", 3),
            ("Spell Book", "items/witch-book.jpg", "Zauberer/in", 1),
            ("Potion", "items/witch-potion.jpg", "Zauberer/in", 2),
            ("Wizard Hat", "items/witch-hat.jpg", "Zauberer/in", 3),
        ]
        cursor.executemany('INSERT INTO items (name, path, rasse, level) VALUES (?, ?, ?, ?)', items)
        print("Items wurden erfolgreich zur Datenbank hinzugefügt.")

    commit_and_close(database)


def get_all_tasks(user_id):
    """
    Ruft alle Aufgaben für einen bestimmten Benutzer aus der Datenbank ab.
    """
    database, cursor = get_database_cursor()
    cursor.execute('SELECT task_id, description, status, deadline FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    commit_and_close(database)
    return tasks
