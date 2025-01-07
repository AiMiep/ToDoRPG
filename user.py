from database import get_database_cursor, commit_and_close

# Neuer User erstellen
# Neuer User erstellen
def create_new_user(username):
    try:
        database, cursor = get_database_cursor()

        # Rasse wählen
        print("Wähle eine Rasse:")
        print("1. Bäcker/in")
        print("2. Maler/in")
        print("3. Zauberer/in")
        rasse_choice = input("Wähle (1-3): ").strip()
        rasse = {"1": "Bäcker/in", "2": "Maler/in", "3": "Zauberer/in"}.get(rasse_choice, "Bäcker/in")

        # Klasse wählen
        print("Wähle eine Klasse:")
        print("1. Anfänger")
        print("2. Fortgeschritten")
        print("3. Profi")
        klasse_choice = input("Wähle (1-3): ").strip()
        klasse = {"1": "Anfänger", "2": "Fortgeschritten", "3": "Profi"}.get(klasse_choice, "Anfänger")

        # Benutzer einfügen
        cursor.execute(''' 
            INSERT INTO users (username, xp, level, rasse, klasse) 
            VALUES (?, ?, ?, ?, ?)
        ''', (username, 0, 1, rasse, klasse))

        commit_and_close(database)
        print(f"Benutzer '{username}' mit Rasse '{rasse}' und Klasse '{klasse}' erfolgreich erstellt.")
    except Exception as e:
        print(f"Fehler beim Erstellen des Benutzers: {e}")


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




