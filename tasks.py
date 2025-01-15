from datetime import datetime

from nicegui import ui

from database import get_database_cursor, commit_and_close
from user import update_user_xp_and_level

def get_valid_date(deadline):
    try:
        date_obj = datetime.strptime(deadline, "%d.%m.%Y").date()

        if date_obj < datetime.now().date():
            return "Datum in der Vergangenheit."
        return None
    except ValueError:
        return "Ungültiges Datum. Bitte verwenden Sie das Format TT.MM.JJJJ."


def create_new_task(difficulty, description, status, current_date, deadline, user_id):
    database, cursor = get_database_cursor()

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

    cursor.execute('''SELECT status, difficulty FROM tasks WHERE task_id = ? AND user_id = ?''', (task_id, user_id))
    task = cursor.fetchone()
    new_status = ""

    if task:
        current_status, difficulty = task
        print(f"Aktueller Status: {current_status}")

        # Überprüfen, ob der Status bereits 'Beendet' ist
        if current_status == 'Beendet':
            print("Aufgabe ist bereits abgeschlossen und kann nicht mehr geändert werden.")
            commit_and_close(database)
            return

        if current_status == 'Erstellt':
            new_status = 'In Bearbeitung'
        elif current_status == 'In Bearbeitung':
            new_status = 'Beendet'

            if difficulty == 'leicht':
                xp_gain = 0.5
            elif difficulty == 'mittel':
                xp_gain = 1
            elif difficulty == 'schwer':
                xp_gain = 1.5
            else:
                xp_gain = 0

            update_user_xp_and_level(user_id, xp_gain)

        cursor.execute('UPDATE tasks SET status = ? WHERE task_id = ? AND user_id = ?', (new_status, task_id, user_id))
        commit_and_close(database)
        print(f"Status wurde zu '{new_status}' geändert.")
    else:
        print("Aufgabe nicht gefunden.")


# Alle Aufgaben anzeigen
def list_all_tasks(user_id):
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM tasks WHERE user_id = ?''', (user_id,))
    tasks = cursor.fetchall()
    database.close()

    if tasks:
        return [task for task in tasks]
    else:
        return []

# Offene Aufgaben anzeigen
def list_all_open_tasks(user_id):
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM tasks WHERE user_id = ? AND status != ?''', (user_id, 'Beendet'))
    tasks = cursor.fetchall()
    database.close()

    if tasks:
        return [task for task in tasks]
    else:
        return []

# Abgeschlossene Aufgaben anzeigen
def list_finished_tasks(user_id):
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM tasks WHERE user_id = ? AND status == ?''', (user_id, 'Beendet'))
    tasks = cursor.fetchall()
    database.close()

    if tasks:
        return [task for task in tasks]
    else:
        return []



# Alle Aufgaben löschen
def delete_all_tasks(user_id):
    confirmation = input("Sicher? (ja/nein): ").lower()
    if confirmation == 'ja':
        database, cursor = get_database_cursor()
        cursor.execute('''DELETE FROM tasks WHERE user_id = ?''', (user_id,))
        commit_and_close(database)
        print("Alle Aufgaben gelöscht.")
    else:
        print("Löschen abgebrochen.")



# Funktion zum Löschen der Aufgabe
def delete_task(user_id, task_id):
    database, cursor = get_database_cursor()

    cursor.execute('''SELECT * FROM tasks WHERE task_id = ? AND user_id = ?''', (task_id, user_id))
    task = cursor.fetchone()

    if task:
        cursor.execute('DELETE FROM tasks WHERE task_id = ? AND user_id = ?', (task_id, user_id))
        commit_and_close(database)
        ui.notify("Aufgabe erfolgreich gelöscht.")
    else:
        ui.notify("Aufgabe nicht gefunden.")