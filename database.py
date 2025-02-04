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


    # Füge neue Items hinzu, ohne alte zu löschen
    items = [
        # Mario-Items (M)
        ("Mario Level 2", "newItems/M-Level1.jpeg", "Mensch (Mario Bros)", 2),
        ("Mario Level 3", "newItems/M-Level2.jpeg", "Mensch (Mario Bros)", 3),
        ("Mario Level 4", "newItems/M-Level3.jpeg", "Mensch (Mario Bros)", 4),
        ("Mario Level 5", "newItems/M-Level4.jpeg", "Mensch (Mario Bros)", 5),
        ("Mario Level 6", "newItems/M-Level5.jpeg", "Mensch (Mario Bros)", 6),
        ("Mario Level 7", "newItems/M-Level6.jpeg", "Mensch (Mario Bros)", 7),
        ("Mario Level 8", "newItems/M-Level7.jpeg", "Mensch (Mario Bros)", 8),
        ("Mario Level 9", "newItems/M-Level8.jpeg", "Mensch (Mario Bros)", 9),
        ("Mario Level 10", "newItems/M-Level9.jpeg", "Mensch (Mario Bros)", 10),

        # Pokémon-Items (P)
        ("Pokémon Level 2", "newItems/P-Level1.jpeg", "Pokémon-Trainer (Pokémon)", 2),
        ("Pokémon Level 3", "newItems/P-Level2.jpeg", "Pokémon-Trainer (Pokémon)", 3),
        ("Pokémon Level 4", "newItems/P-Level3.jpeg", "Pokémon-Trainer (Pokémon)", 4),
        ("Pokémon Level 5", "newItems/P-Level4.jpeg", "Pokémon-Trainer (Pokémon)", 5),
        ("Pokémon Level 6", "newItems/P-Level5.jpg", "Pokémon-Trainer (Pokémon)", 6),
        ("Pokémon Level 7", "newItems/P-Level6.jpeg", "Pokémon-Trainer (Pokémon)", 7),
        ("Pokémon Level 8", "newItems/P-Level7.jpeg", "Pokémon-Trainer (Pokémon)", 8),
        ("Pokémon Level 9", "newItems/P-Level8.jpeg", "Pokémon-Trainer (Pokémon)", 9),
        ("Pokémon Level 10", "newItems/P-Level9.jpg", "Pokémon-Trainer (Pokémon)", 10),

        # Zelda-Items (Z)
        ("Zelda Level 2", "newItems/Z-Level1.jpeg", "Goronen/Zoras/Rito/Gerudo (Zelda)", 2),
        ("Zelda Level 3", "newItems/Z-Level2.jpeg", "Goronen/Zoras/Rito/Gerudo (Zelda)", 3),
        ("Zelda Level 4", "newItems/Z-Level3.jpeg", "Goronen/Zoras/Rito/Gerudo (Zelda)", 4),
        ("Zelda Level 5", "newItems/Z-Level4.jpeg", "Goronen/Zoras/Rito/Gerudo (Zelda)", 5),
        ("Zelda Level 6", "newItems/Z-Level5.jpeg", "Goronen/Zoras/Rito/Gerudo (Zelda)", 6),
        ("Zelda Level 7", "newItems/Z-Level6.jpeg", "Goronen/Zoras/Rito/Gerudo (Zelda)", 7),
        ("Zelda Level 8", "newItems/Z-Level7.jpeg", "Goronen/Zoras/Rito/Gerudo (Zelda)", 8),
        ("Zelda Level 9", "newItems/Z-Level8.jpeg", "Goronen/Zoras/Rito/Gerudo (Zelda)", 9),
        ("Zelda Level 10", "newItems/Z-Level9.jpeg", "Goronen/Zoras/Rito/Gerudo (Zelda)", 10),
    ]

    for name, path, rasse, level in items:
        # Prüfe, ob das Item bereits existiert
        cursor.execute('SELECT COUNT(*) FROM items WHERE name = ? AND rasse = ? AND level = ?', (name, rasse, level))
        if cursor.fetchone()[0] == 0:
            # Füge das Item nur hinzu, wenn es noch nicht existiert
            cursor.execute('INSERT INTO items (name, path, rasse, level) VALUES (?, ?, ?, ?)',
                           (name, path, rasse, level))
            print(f"Item hinzugefügt: {name} (Rasse: {rasse}, Level: {level})")

    commit_and_close(database)
    print("Neue Items wurden erfolgreich hinzugefügt (nur fehlende Items).")
