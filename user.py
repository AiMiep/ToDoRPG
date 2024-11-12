from database import get_database_cursor, commit_and_close
import sqlite3

# Neuer User erstellen
def create_new_user(email, name, age, gender, password):
    database, cursor = get_database_cursor()

    try:
        cursor.execute('''
            INSERT INTO users (email, username, age, gender, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, name, age, gender, password))

        commit_and_close(database)
        print(f"Benutzer '{name}' erfolgreich registriert.")
    except sqlite3.IntegrityError:
        print("Ein Benutzer mit dieser E-Mail-Adresse existiert bereits.")

# Alle User anzeigen
def list_all_user():
    database, cursor = get_database_cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    if users:
        print(f"{'ID':<5} | {'E-Mail':<20} | {'Name':<10} | {'Alter':<10} | {'Geschlecht':<10}")
        print("-" * 60)
        for user in users:
            print(f"{user[0]:<5} | {user[1]:<20} | {user[2]:<10} | {user[3]:<10}")
    else:
        print("Keine User vorhanden.")

# User löschen
def delete_user(email):
    database, cursor = get_database_cursor()

    cursor.execute('DELETE FROM users WHERE email = ?', (email,))
    commit_and_close(database)

    print(f"User mit E-Mail: {email} erfolgreich gelöscht.")

