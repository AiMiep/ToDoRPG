from nicegui import ui
from database import get_database_cursor, commit_and_close


def get_all_avatars():
    """
    Ruft alle Avatare aus der Datenbank ab.
    """
    database, cursor = get_database_cursor()
    cursor.execute('SELECT avatar_id, name, path FROM avatars')  # Stelle sicher, dass 'path' enthalten ist
    avatars = cursor.fetchall()
    commit_and_close(database)
    print("DEBUG - Avatare aus der Datenbank:", avatars)  # Debug-Ausgabe für Avatare
    return avatars


from database import get_database_cursor, commit_and_close

def initialize_user():
    """
    Prüft, ob ein Benutzer existiert.
    Gibt True zurück, wenn ein Benutzer existiert, andernfalls False.
    """
    database, cursor = get_database_cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    result = cursor.fetchone()
    commit_and_close(database)

    print(f"DEBUG: Anzahl der Benutzer in der Datenbank: {result[0]}")
    return result[0] > 0


def check_if_user_exists():
    database, cursor = get_database_cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    result = cursor.fetchone()
    commit_and_close(database)

    print(f"DEBUG: Anzahl der Benutzer in der Datenbank: {result[0]}")  # Debug-Ausgabe
    return result[0] > 0


def create_new_user(username, rasse, klasse, avatar_id):
    try:
        database, cursor = get_database_cursor()

        # Prüfen, ob der Benutzername bereits existiert
        cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            print(f"Fehler: Der Benutzername '{username}' ist bereits vergeben.")
            commit_and_close(database)  # Sicherstellen, dass die Verbindung geschlossen wird
            return

        # Benutzer in die Datenbank einfügen
        cursor.execute('''
            INSERT INTO users (username, xp, level, rasse, klasse, avatar_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, 0, 1, rasse, klasse, avatar_id))

        # Änderungen speichern und Verbindung schließen
        commit_and_close(database)

        # Debug-Ausgabe zur Überprüfung
        print(f"DEBUG: Benutzer '{username}' wurde erfolgreich in der Datenbank gespeichert.")
    except Exception as e:
        print(f"Fehler beim Erstellen des Benutzers: {e}")


from database import get_database_cursor, commit_and_close

def update_user_avatar(user_id, avatar_id):
    """
    Aktualisiert den Avatar eines Benutzers in der Datenbank.
    """
    try:
        database, cursor = get_database_cursor()
        cursor.execute('UPDATE users SET avatar_id = ? WHERE user_id = ?', (avatar_id, user_id))
        commit_and_close(database)
        print(f"Avatar für Benutzer {user_id} erfolgreich auf {avatar_id} geändert.")
    except Exception as e:
        print(f"Fehler beim Ändern des Avatars: {e}")



def update_race_and_class(user_id, rasse, klasse):
    """
    Ändert die Rasse und Klasse des Benutzers.
    """
    try:
        database, cursor = get_database_cursor()
        cursor.execute('''
            UPDATE users
            SET rasse = ?, klasse = ?
            WHERE user_id = ?
        ''', (rasse, klasse, user_id))
        commit_and_close(database)
        print(f"Rasse und Klasse erfolgreich geändert zu: Rasse '{rasse}', Klasse '{klasse}'.")
    except Exception as e:
        print(f"Fehler beim Aktualisieren von Rasse und Klasse: {e}")


def print_user_data():
    """
    Gibt alle Benutzerinformationen aus der Datenbank zurück.
    """
    database, cursor = get_database_cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    commit_and_close(database)

    if users:
        return {user[0]: {"username": user[1], "xp": user[2], "level": user[3], "rasse": user[4], "klasse": user[5]} for user in users}
    else:
        return {}

def refresh_user_data(user_id):
    """
    Aktualisiert die UI mit den neuesten Benutzerinformationen.
    """
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
    """
    Aktualisiert die XP und das Level eines Benutzers. Belohnungen gibt es nur bei einem Level-Up.
    """
    try:
        database, cursor = get_database_cursor()
        cursor.execute('SELECT xp, level, rasse FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            print(f"Fehler: Benutzer mit ID {user_id} wurde nicht gefunden.")
            commit_and_close(database)
            return

        current_xp, current_level, rasse = user
        print(f"DEBUG: Vorher - XP: {current_xp}, Level: {current_level}")

        new_xp = current_xp + xp_gain
        new_level = current_level

        # Prüfen, ob ein Level-Up erreicht wird
        if new_xp >= 3:
            new_level += 1
            new_xp -= 3
            print(f"DEBUG: Level-Up! Neues Level: {new_level}, Rest-XP: {new_xp}")

        # Update in der Datenbank
        cursor.execute('UPDATE users SET xp = ?, level = ? WHERE user_id = ?', (new_xp, new_level, user_id))

        # Belohnung nur bei einem Level-Up
        if new_level > current_level:
            cursor.execute('SELECT item_id, name, path FROM items WHERE rasse = ? AND level = ?', (rasse, new_level))
            item = cursor.fetchone()
            if item:
                item_id, item_name, item_path = item
                cursor.execute('INSERT INTO user_items (user_id, item_id) VALUES (?, ?)', (user_id, item_id))
                print(f"DEBUG: Belohnung hinzugefügt: {item_name} (ID: {item_id})")

                # Belohnung anzeigen
                with ui.dialog() as dialog, ui.card():
                    ui.label(f'Belohnung erhalten: {item_name}').classes('text-bold')
                    ui.image(f'/images/{item_path}').classes('w-64 h-64')
                    ui.button('Schließen', on_click=dialog.close)
                    dialog.open()

        commit_and_close(database)
        print(f"DEBUG: Nachher - XP: {new_xp}, Level: {new_level}")

        # UI aktualisieren
        refresh_user_data(user_id)

    except Exception as e:
        print(f"Fehler beim Aktualisieren von XP und Level: {e}")


def show_user_items(user_id):
    """
    Zeigt alle gesammelten Items des Benutzers an.
    """
    try:
        database, cursor = get_database_cursor()
        cursor.execute('''
            SELECT i.name, i.path
            FROM user_items ui
            JOIN items i ON ui.item_id = i.item_id
            WHERE ui.user_id = ?
        ''', (user_id,))
        items = cursor.fetchall()
        commit_and_close(database)
        return items if items else []
    except Exception as e:
        print(f"Fehler beim Abrufen der Benutzer-Items: {e}")
        return []

from database import get_database_cursor, commit_and_close

def get_all_users():
    """
    Ruft alle Benutzer aus der Datenbank ab.
    Gibt eine Liste von Tupeln mit Benutzerinformationen zurück.
    """
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
    """
    Ruft die Informationen eines bestimmten Benutzers anhand der Benutzer-ID ab.
    Gibt ein Tupel mit Benutzerinformationen zurück oder None, falls der Benutzer nicht existiert.
    """
    try:
        database, cursor = get_database_cursor()
        cursor.execute('SELECT username, rasse, klasse, avatar_id, level, xp FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        commit_and_close(database)
        return user
    except Exception as e:
        print(f"Fehler beim Abrufen des Benutzers mit ID {user_id}: {e}")
        return None

# def switch_user(new_user_id):
#     """
#     Wechselt den aktuellen Benutzer.
#     """
#     global user_id
#     user_id = new_user_id
#     ui.notify(f'Benutzer erfolgreich gewechselt! Neuer Benutzer-ID: {user_id}', color='positive')

def select_avatar(avatar_id):
    """
    Speichert den ausgewählten Avatar für den aktuellen Benutzer.
    """
    global user_id
    update_user_avatar(user_id, avatar_id)
    ui.notify(f"Avatar erfolgreich geändert! Neuer Avatar-ID: {avatar_id}", color='positive')

def select_user(selected_user_id):
    """
    Aktualisiert die globale Benutzer-ID.
    """
    global user_id
    user_id = selected_user_id
    print(f"DEBUG: Benutzer-ID wurde auf {user_id} gesetzt.")
    ui.notify(f"Benutzer erfolgreich gewechselt! Neue Benutzer-ID: {user_id}", color='positive')
