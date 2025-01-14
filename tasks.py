from datetime import date
from database import get_database_cursor, commit_and_close
from user import update_user_xp_and_level
import utils


def create_new_task(user_id, description=None, deadline=None, difficulty=None):
    if not description:
        description = input("Beschreibung: ")
    if not deadline:
        deadline = utils.get_valid_date()
    if not difficulty:
        print("Schwierigkeitsstufen:")
        print("1. leicht")
        print("2. mittel")
        print("3. schwer")
        answer_difficulty = input("Wähle die Schwierigkeitsstufe: ")
        difficulty = {'1': 'leicht', '2': 'mittel', '3': 'schwer'}.get(answer_difficulty, 'leicht')

    database, cursor = get_database_cursor()
    status = 'Erstellt'
    current_date = date.today()

    cursor.execute('''
        INSERT INTO tasks (difficulty, description, status, date, deadline, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (difficulty, description, status, current_date, deadline, user_id))

    commit_and_close(database)
    print(f"Aufgabe '{description}' erfolgreich erstellt.")


def update_task_status(user_id, task_id):
    database, cursor = get_database_cursor()

    cursor.execute('SELECT status, difficulty FROM tasks WHERE task_id = ? AND user_id = ?', (task_id, user_id))
    task = cursor.fetchone()
    new_status = ""

    if task:
        current_status, difficulty = task
        print(f"Aktueller Status: {current_status}")

        if current_status == 'Beendet':
            print("Aufgabe ist bereits abgeschlossen und kann nicht mehr geändert werden.")
            commit_and_close(database)
            return

        if current_status == 'Erstellt':
            new_status = 'In Bearbeitung'
        elif current_status == 'In Bearbeitung':
            new_status = 'Beendet'

        xp_gain = {'leicht': 0.5, 'mittel': 1, 'schwer': 1.5}.get(difficulty, 0)
        update_user_xp_and_level(user_id, xp_gain)

        cursor.execute('UPDATE tasks SET status = ? WHERE task_id = ? AND user_id = ?', (new_status, task_id, user_id))
        commit_and_close(database)
        print(f"Status wurde zu '{new_status}' geändert.")
    else:
        print("Aufgabe nicht gefunden.")
        commit_and_close(database)


def list_all_tasks(user_id):
    database, cursor = get_database_cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()

    commit_and_close(database)
    return tasks if tasks else []


def list_all_open_tasks(user_id):
    database, cursor = get_database_cursor()

    cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND status != ?', (user_id, 'Beendet'))
    tasks = cursor.fetchall()

    commit_and_close(database)
    return tasks if tasks else []


def list_finished_tasks(user_id):
    database, cursor = get_database_cursor()

    cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND status == ?', (user_id, 'Beendet'))
    tasks = cursor.fetchall()

    commit_and_close(database)
    return tasks if tasks else []


def delete_all_tasks(user_id):
    confirmation = input("Sicher? (ja/nein): ").lower()
    if confirmation == 'ja':
        database, cursor = get_database_cursor()
        cursor.execute('DELETE FROM tasks WHERE user_id = ?', (user_id,))
        commit_and_close(database)
        print("Alle Aufgaben gelöscht.")
    else:
        print("Löschen abgebrochen.")


def delete_task(user_id, task_id=None):
    if not task_id:
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
