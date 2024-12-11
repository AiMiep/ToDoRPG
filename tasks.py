from datetime import date, datetime
from database import get_database_cursor, commit_and_close
import utils

def create_new_task(user_id):
    description = input("Beschreibung: ")
    deadline = utils.get_valid_date()

    # Schwierigkeitsstufe auswählen
    print("Schwierigkeitsstufen:")
    print("1. leicht")
    print("2. mittel")
    print("3. schwer")
    answer_difficulty = input("Wähle die Schwierigkeitsstufe: ")

    # Schwierigkeitsstufe zuweisen
    if answer_difficulty == "1":
        difficulty = "leicht"
    elif answer_difficulty == "2":
        difficulty = "mittel"
    elif answer_difficulty == "3":
        difficulty = "schwer"
    else:
        print("Ungültige Auswahl. Standardwert 'leicht' verwendet.")
        difficulty = "leicht"

    # Aufgabe in die Datenbank einfügen
    database, cursor = get_database_cursor()
    status = 'Erstellt'
    current_date = date.today()

    cursor.execute('''
          INSERT INTO tasks (difficulty, description, status, date, deadline, user_id) 
          VALUES (?, ?, ?, ?, ?, ?)
      ''', (difficulty, description, status, current_date, deadline, user_id))

    commit_and_close(database)
    print(f"Aufgabe '{description}' erfolgreich erstellt.")

# Status einer Aufgabe ändern
def update_task_status(user_id):
    task_id = input("Aufgaben-ID: ")

    database, cursor = get_database_cursor()
    cursor.execute('SELECT status FROM tasks WHERE task_id = ? AND user_id = ?', (task_id, user_id))
    task = cursor.fetchone()

    if task:
        current_status = task[0]
        print(f"Aktueller Status: {current_status}")

        if current_status == 'Erstellt':
            new_status = 'In Bearbeitung'
        elif current_status == 'In Bearbeitung':
            new_status = 'Beendet'
        elif current_status == 'Beendet':
            print("Die Aufgabe ist bereits abgeschlossen. Keine Änderungen mehr möglich.")
            database.close()
            return
        else:
            print("Unbekannter Status.")
            database.close()
            return

        cursor.execute('UPDATE tasks SET status = ? WHERE task_id = ? AND user_id = ?', (new_status, task_id, user_id))
        commit_and_close(database)
        print(f"Status erfolgreich auf '{new_status}' geändert.")

    else:
        print("Aufgabe nicht gefunden.")


# Alle Aufgaben anzeigen
def list_all_tasks(user_id):
    database, cursor = get_database_cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()

    if tasks:
        for task in tasks:
            print(task)
    else:
        print("LEER")

# Alle Aufgaben anzeigen (außer abgeschlossene Aufgaben)
def list_all_open_tasks(user_id):
    database, cursor = get_database_cursor()

    cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND status != ?', (user_id, 'Beendet'))
    tasks = cursor.fetchall()

    if tasks:
        for task in tasks:
            print(task)
    else:
        print("LEER")

# Abgeschlossene Aufgaben anzeigen
def list_finished_tasks(user_id):
    database, cursor = get_database_cursor()

    cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND status == ?', (user_id, 'Beendet'))
    tasks = cursor.fetchall()

    if tasks:
        for task in tasks:
            print(task)
    else:
        print("LEER")

# Alle Aufgaben löschen
def delete_all_tasks(user_id):
    confirmation = input("Sicher? (ja/nein): ").lower()
    if confirmation == 'ja':
        database, cursor = get_database_cursor()
        cursor.execute('DELETE FROM tasks WHERE user_id = ?', (user_id,))
        commit_and_close(database)
        print("Alle Aufgaben gelöscht.")
    else:
        print("Löschen abgebrochen.")

# Einzelne Aufgabe löschen
def delete_task(user_id):
    task_id = input("Aufgaben-ID: ")
    database, cursor = get_database_cursor()

    cursor.execute('SELECT * FROM tasks WHERE task_id = ? AND user_id = ?', (task_id, user_id))
    task = cursor.fetchone()

    if task:
        confirmation = input("Sicher? (ja/nein): ").lower()
        if confirmation == 'ja':
            cursor.execute('DELETE FROM tasks WHERE task_id = ? AND user_id = ?', (task_id, user_id))
            commit_and_close(database)
            print("Aufgabe gelöscht.")
        else:
            print("Löschen abgebrochen.")
    else:
        print("Aufgabe nicht gefunden.")
        database.close()
