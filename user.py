from nicegui import ui
from database import get_database_cursor, commit_and_close

def initialize_user():
    """Prüft, ob ein Benutzer existiert."""
    database, cursor = get_database_cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    result = cursor.fetchone()
    commit_and_close(database)
    print(f"DEBUG: Anzahl der Benutzer in der Datenbank: {result[0]}")
    return result[0] > 0

def create_new_user(username, rasse, klasse, avatar_id):
    """Erstellt einen neuen Benutzer mit den angegebenen Details."""
    try:
        database, cursor = get_database_cursor()

        # Prüfen, ob der Benutzername bereits existiert
        cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            print(f"Fehler: Der Benutzername '{username}' ist bereits vergeben.")
            return

        # Benutzer in die Datenbank einfügen
        cursor.execute('''
            INSERT INTO users (username, xp, level, rasse, klasse, avatar_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, 0, 1, rasse, klasse, avatar_id))

        # Benutzer-ID des neu erstellten Benutzers abrufen
        user_id = cursor.lastrowid
        print(f"DEBUG: Neuer Benutzer erstellt mit ID {user_id}, Rasse: {rasse}")

        # Vergibt das Level-1-Item basierend auf der Rasse (still im Hintergrund)
        item_name, item_path = assign_item_on_level_up(user_id, rasse, 1)
        if item_name:
            print(f"DEBUG: Benutzer erhält Level-1-Item: {item_name}")

    except Exception as e:
        print(f"Fehler beim Erstellen des Benutzers: {e}")
    finally:
        # Verbindung immer schließen
        commit_and_close(database)

def get_all_users():
    """Ruft alle Benutzer aus der Datenbank ab."""
    try:
        database, cursor = get_database_cursor()
        cursor.execute('SELECT user_id, username, rasse, klasse, avatar_id, level, xp FROM users')
        users = cursor.fetchall()
        commit_and_close(database)
        return users
    except Exception as e:
        print(f"Fehler beim Abrufen aller Benutzer: {e}")
        return []

def get_user_by_id(user_id):
    """Ruft die Informationen eines Benutzers anhand seiner ID ab."""
    try:
        database, cursor = get_database_cursor()
        cursor.execute('SELECT username, rasse, klasse, avatar_id, level, xp FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        commit_and_close(database)
        return user
    except Exception as e:
        print(f"Fehler beim Abrufen des Benutzers mit ID {user_id}: {e}")
        return None

def update_user_avatar(user_id, avatar_id):
    """Aktualisiert den Avatar eines Benutzers."""
    try:
        database, cursor = get_database_cursor()
        cursor.execute('UPDATE users SET avatar_id = ? WHERE user_id = ?', (avatar_id, user_id))
        commit_and_close(database)
        print(f"Avatar für Benutzer {user_id} erfolgreich aktualisiert.")
    except Exception as e:
        print(f"Fehler beim Aktualisieren des Avatars: {e}")

def update_race_and_class(user_id, rasse, klasse):
    """Aktualisiert die Rasse und Klasse eines Benutzers."""
    try:
        database, cursor = get_database_cursor()
        cursor.execute('''
            UPDATE users
            SET rasse = ?, klasse = ?
            WHERE user_id = ?
        ''', (rasse, klasse, user_id))
        commit_and_close(database)
        print(f"Rasse und Klasse für Benutzer {user_id} erfolgreich aktualisiert.")
    except Exception as e:
        print(f"Fehler beim Aktualisieren von Rasse und Klasse: {e}")

def print_user_data():
    """Gibt alle Benutzerdaten aus der Datenbank zurück."""
    database, cursor = get_database_cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    commit_and_close(database)

    if users:
        return {
            user[0]: {
                "username": user[1],
                "xp": user[2],
                "level": user[3],
                "rasse": user[4],
                "klasse": user[5],
                "avatar_id": user[6],
            }
            for user in users
        }
    else:
        return {}

def refresh_user_data(user_id):
    """Aktualisiert die UI mit den neuesten Benutzerdaten."""
    try:
        database, cursor = get_database_cursor()
        cursor.execute('SELECT xp, level FROM users WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()
        commit_and_close(database)

        if user_data:
            xp, level = user_data
            print(f"DEBUG: Benutzer-ID {user_id} - XP: {xp}, Level: {level}")
            ui.notify(f"XP: {xp}, Level: {level}", color='positive')
        else:
            print(f"Fehler: Benutzer mit ID {user_id} nicht gefunden.")
    except Exception as e:
        print(f"Fehler beim Aktualisieren der Benutzeroberfläche: {e}")

def update_user_xp_and_level(user_id, xp_gain):
    """Aktualisiert die XP und das Level eines Benutzers. Vergibt Belohnungen bei Level-Ups."""
    try:
        database, cursor = get_database_cursor()
        cursor.execute('SELECT xp, level, rasse FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            print(f"Fehler: Benutzer mit ID {user_id} wurde nicht gefunden.")
            commit_and_close(database)
            return

        current_xp, current_level, rasse = user
        new_xp = current_xp + xp_gain
        new_level = current_level

        # Prüfen, ob ein Level-Up erreicht wird
        if new_xp >= 3:
            new_level += 1
            new_xp -= 3

            # Item vergeben
            item_name, item_path = assign_item_on_level_up(user_id, rasse, new_level)
            if item_name and item_path:
                with ui.dialog() as dialog:
                    with ui.card():
                        ui.label(f"🎉 Glückwunsch zum Level-Up auf Level {new_level}!").classes('text-2xl font-bold')
                        ui.image(f'/images/{item_path}').classes('w-32 h-32 object-cover rounded-full')
                        ui.label(f"Du hast das Item '{item_name}' erhalten!").classes('text-lg')
                        ui.button("Schließen", on_click=dialog.close).classes('bg-blue-500 text-white rounded-md')
                    dialog.open()

        # Update in der Datenbank
        cursor.execute('UPDATE users SET xp = ?, level = ? WHERE user_id = ?', (new_xp, new_level, user_id))
        commit_and_close(database)

        # UI aktualisieren
        refresh_user_data(user_id)

    except Exception as e:
        print(f"Fehler beim Aktualisieren von XP und Level: {e}")

def select_user(selected_user_id):
    """
    Aktualisiert die globale Benutzer-ID.
    """
    global user_id
    user_id = selected_user_id
    print(f"DEBUG: Benutzer-ID wurde auf {user_id} gesetzt.")
    ui.notify(f"Benutzer erfolgreich gewechselt! Neue Benutzer-ID: {user_id}", color='positive')

def assign_item_on_level_up(user_id, rasse, level):
    """Vergibt ein Item basierend auf Rasse und Level (ab Level 2)."""
    try:
        # Nur ab Level 2 vergeben
        if level < 2:
            print(f"DEBUG: Kein Item für Level {level}, da Items erst ab Level 2 vergeben werden.")
            return None, None

        database, cursor = get_database_cursor()
        print(f"DEBUG: Vergabe eines Items für Benutzer {user_id}, Rasse: {rasse}, Level: {level}")

        # Suche nach einem passenden Item basierend auf Rasse und Level
        cursor.execute(
            'SELECT item_id, name, path FROM items WHERE rasse = ? AND level = ?',
            (rasse, level)
        )
        item = cursor.fetchone()
        if item:
            item_id, item_name, item_path = item
            print(f"DEBUG: Gefundenes Item: {item_name}, Pfad: {item_path}")

            # Verknüpfe das Item mit dem Benutzer
            cursor.execute(
                'INSERT INTO user_items (user_id, item_id) VALUES (?, ?)',
                (user_id, item_id)
            )
            database.commit()  # Änderungen speichern
            return item_name, item_path
        else:
            print(f"DEBUG: Kein Item für Rasse '{rasse}' und Level {level} gefunden.")
            return None, None
    except Exception as e:
        print(f"Fehler beim Zuweisen eines Items: {e}")
        return None, None
    finally:
        commit_and_close(database)

