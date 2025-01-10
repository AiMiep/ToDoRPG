from database import get_database_cursor, commit_and_close

# Neuer User erstellen
def create_new_user(username):
    try:
        database, cursor = get_database_cursor()

        # Prüfen, ob der Benutzername bereits existiert
        cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            print(f"Fehler: Der Benutzername '{username}' ist bereits vergeben. Bitte wähle einen anderen Namen.")
            return

        # Rasse auswählen
        print("Wähle eine Rasse:")
        print("1. Bäcker/in")
        print("2. Maler/in")
        print("3. Zauberer/in")
        rasse_choice = input("Wähle (1-3): ").strip()
        rasse = {"1": "Bäcker/in", "2": "Maler/in", "3": "Zauberer/in"}.get(rasse_choice, "Bäcker/in")

        # Klasse auswählen
        print("Wähle eine Klasse:")
        print("1. Anfänger")
        print("2. Fortgeschritten")
        print("3. Profi")
        klasse_choice = input("Wähle (1-3): ").strip()
        klasse = {"1": "Anfänger", "2": "Fortgeschritten", "3": "Profi"}.get(klasse_choice, "Anfänger")

        # Avatar auswählen
        print("Wähle einen Avatar:")
        cursor.execute('SELECT avatar_id, name FROM avatars')
        avatars = cursor.fetchall()

        if not avatars:
            print("Fehler: Es sind keine Avatare in der Datenbank vorhanden.")
            return

        for avatar in avatars:
            print(f"{avatar[0]}. {avatar[1]}")
        avatar_choice = input("Wähle einen Avatar (ID): ").strip()
        avatar_id = int(avatar_choice) if avatar_choice.isdigit() and int(avatar_choice) in [a[0] for a in avatars] else avatars[0][0]

        # Benutzer in die Datenbank einfügen
        cursor.execute(''' 
            INSERT INTO users (username, xp, level, rasse, klasse, avatar_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, 0, 1, rasse, klasse, avatar_id))

        commit_and_close(database)
        print(f"Benutzer '{username}' mit Rasse '{rasse}', Klasse '{klasse}' und Avatar erfolgreich erstellt.")
    except Exception as e:
        print(f"Fehler beim Erstellen des Benutzers: {e}")

# Avatar ändern
def update_avatar(user_id):
    try:
        database, cursor = get_database_cursor()

        print("Wähle einen neuen Avatar:")
        cursor.execute('SELECT avatar_id, name FROM avatars')
        avatars = cursor.fetchall()
        for avatar in avatars:
            print(f"{avatar[0]}. {avatar[1]}")
        avatar_choice = input("Wähle einen Avatar (ID): ").strip()
        avatar_id = int(avatar_choice) if avatar_choice.isdigit() and int(avatar_choice) in [a[0] for a in avatars] else avatars[0][0]

        cursor.execute('UPDATE users SET avatar_id = ? WHERE user_id = ?', (avatar_id, user_id))
        commit_and_close(database)
        print(f"Avatar erfolgreich geändert zu '{avatar_id}'.")
    except Exception as e:
        print(f"Fehler beim Aktualisieren des Avatars: {e}")

# Rasse und Klasse ändern
def update_race_and_class(user_id):
    try:
        database, cursor = get_database_cursor()

        # Neue Rasse wählen
        print("Wähle eine neue Rasse:")
        print("1. Bäcker/in")
        print("2. Maler/in")
        print("3. Zauberer/in")
        rasse_choice = input("Wähle (1-3): ").strip()
        rasse = {"1": "Bäcker/in", "2": "Maler/in", "3": "Zauberer/in"}.get(rasse_choice, "Bäcker/in")

        # Neue Klasse wählen
        print("Wähle eine neue Klasse:")
        print("1. Anfänger")
        print("2. Fortgeschritten")
        print("3. Profi")
        klasse_choice = input("Wähle (1-3): ").strip()
        klasse = {"1": "Anfänger", "2": "Fortgeschritten", "3": "Profi"}.get(klasse_choice, "Anfänger")

        # Update ausführen
        cursor.execute('''
            UPDATE users 
            SET rasse = ?, klasse = ? 
            WHERE user_id = ?
        ''', (rasse, klasse, user_id))

        commit_and_close(database)
        print(f"Rasse und Klasse erfolgreich geändert zu: Rasse '{rasse}', Klasse '{klasse}'.")
    except Exception as e:
        print(f"Fehler beim Aktualisieren von Rasse und Klasse: {e}")



def check_if_user_exists():
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT COUNT(*) FROM users''')
    result = cursor.fetchone()

    if result[0] == 0:
        username = input("Gebe bitte einen Benutzernamen ein: ")
        create_new_user(username)
    else:
        print("User bereits erstellt.")


def print_user_data():
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM users''')
    users = cursor.fetchall()

    if users:
        print(users)
    else:
        print("Keine Benutzer gefunden.")

    commit_and_close(database)


def update_user_xp_and_level(user_id, xp_gain):
    database, cursor = get_database_cursor()

    cursor.execute('''SELECT xp, level FROM users WHERE users_id = ?''', (user_id,))
    user = cursor.fetchone()

    if user:
        current_xp, current_lvl = user
        new_xp = current_xp + xp_gain

        if new_xp >= 3:
            new_lvl = current_lvl + 1
            new_xp = 0
        else:
            new_lvl = current_lvl

        cursor.execute('''UPDATE users SET xp = ?, level = ? WHERE users_id = ?''', (new_xp, new_lvl, user_id))

    commit_and_close(database)




