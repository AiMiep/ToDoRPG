from datetime import datetime
from tasks import create_new_task, list_all_tasks, update_task_status, delete_task, delete_all_tasks
from user import create_new_user, delete_user, list_all_user
from database import get_database_cursor, commit_and_close
import sqlite3

def get_valid_date():
    while True:
        deadline = input("Fälligkeitsdatum (TT.MM.JJJJ): ")
        try:
            date_obj = datetime.strptime(deadline, "%d.%m.%Y").date()
            if date_obj < datetime.now().date():
                print("Datum liegt in der Vergangenheit.")
                continue
            return date_obj
        except ValueError:
            print("Ungültiges Datum. Bitte verwenden Sie das Format TT.MM.JJJJ.")

def show_task_options():
    print("\nTask-Manager")
    print("1. Aufgabe erstellen")
    print("2. Aufgaben anzeigen")
    print("3. Aufgabe aktualisieren")
    print("4. Aufgabe löschen")
    print("5. Alle Aufgaben löschen")
    print("6. Beenden")

def task_manager(user_email):
    while True:
        show_task_options()
        option = input("Wähle eine Option (1-6): ")

        if option == '1':
            description = input("Beschreibung: ")
            deadline = get_valid_date()
            create_new_task(description, deadline, user_email)

        elif option == '2':
            list_all_tasks(user_email)

        elif option == '3':
            task_id = int(input("ID der zu aktualisierenden Aufgabe: "))
            new_status = input("Neuer Status: ")
            update_task_status(task_id, new_status, user_email)

        elif option == '4':
            task_id = int(input("ID der zu löschenden Aufgabe: "))
            delete_task(task_id, user_email)

        elif option == '5':
            delete_all_tasks(user_email)

        elif option == '6':
            print("Task-Manager beendet.")
            break

        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")

def show_user_options():
    print("\nUser-Manager")
    print("1. Neuen User erstellen")
    print("2. Alle User anzeigen")
    print("3. User löschen")
    print("4. Beenden")

def user_manager():
    logged_in = False
    user_email = ""
    while True:
        if not logged_in:
            logged_in = show_login_options()
            continue

        show_user_options()
        option = input("Wähle eine Option (1-4): ")

        if option == '1':
            email = input("E-Mail: ")
            username = input("Name: ")
            age = input("Alter: ")
            gender = input("Geschlecht: ")
            password = input("Passwort: ")  # Passwort für den neuen Benutzer
            create_new_user(email, username, age, gender, password)
        elif option == '2':
            list_all_user()
        elif option == '3':
            email = input("E-Mail des zu löschenden Users: ")
            delete_user(email)
        elif option == '4':
            print("User-Manager beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")


def show_login_options():
    choice = input("Möchtest du dich anmelden (1) oder registrieren (2)? ")

    if choice == '1':
        email = input("E-Mail: ")
        password = input("Passwort: ")
        return login_user(email, password)

    elif choice == '2':
        # Registrierung
        email = input("E-Mail: ")
        name = input("Name: ")
        age = input("Alter: ")
        gender = input("Geschlecht: ")
        password = input("Passwort: ")
        return register_user(email, name, age, gender, password)

    else:
        print("Ungültige Auswahl.")
        return None


def login_user(email, password):
    database, cursor = get_database_cursor()

    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()

    if user:
        print(f"Willkommen, {user[1]}!")
        return email
    else:
        print("Ungültige Anmeldedaten.")
        return None


def register_user(email, name, age, gender, password):
    database, cursor = get_database_cursor()

    try:
        cursor.execute('''
              INSERT INTO users (email, username, age, gender, password)
              VALUES (?, ?, ?, ?, ?)
          ''', (email, name, age, gender, password))

        commit_and_close(database)
        print(f"Benutzer '{name}' erfolgreich registriert.")
        return email
    except sqlite3.IntegrityError:
        print("Ein Benutzer mit dieser E-Mail-Adresse existiert bereits.")
        return None

