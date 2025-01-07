from database import get_database_cursor, commit_and_close


# Neuer User erstellen
def create_new_user(username):
    database, cursor = get_database_cursor()
    xp = 0
    level = 1
    cursor.execute(''' 
        INSERT INTO users (username, xp, level) 
        VALUES (?,?,?)
    ''', (username, xp, level))

    commit_and_close(database)
    print(f"Benutzer '{username}' erfolgreich erstellt.")


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

