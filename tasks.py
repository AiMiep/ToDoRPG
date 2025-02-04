from datetime import datetime
from nicegui import ui
from database import get_database_cursor, commit_and_close
from user import update_user_xp_and_level


def check_date_validation(deadline):
    """
    Prüft, ob sich das Datum in der Vergangenheit befindet oder ungültige Werte eingegeben wurde.
    """
    try:
        date_obj = datetime.strptime(deadline, "%d.%m.%Y").date()

        if date_obj < datetime.now().date():
            return "❌ Datum ist in der Vergangenheit!"
        return None
    except ValueError:
        return "❌ Bitte überprüfe die Eingaben..."


def create_new_task(difficulty, description, status, current_date, deadline, user_id):
    """
    Erstellt eine neue Aufgabe und speichert diese in die Datenbank
    """

    database, cursor = get_database_cursor()

    cursor.execute('''
          INSERT INTO tasks (difficulty, description, status, date, deadline, user_id) 
          VALUES (?, ?, ?, ?, ?, ?)
      ''', (difficulty, description, status, current_date, deadline, user_id))

    commit_and_close(database)


def edit_task_attributes(user_id, task_id, description_input, deadline_input, difficulty_input, error_message):
    """
    Ermöglicht die Datenänderung von bestehenden Aufgaben und das Aktualisieren der Daten in der Datenbank
    """

    new_description = description_input.value
    new_deadline = deadline_input.value
    new_difficulty = difficulty_input.value

    database, cursor = get_database_cursor()
    cursor.execute('SELECT * FROM tasks WHERE task_id = ? AND user_id = ?', (task_id, user_id))
    task = cursor.fetchone()

    if task:
        if new_description:
            cursor.execute(
                'UPDATE tasks SET description = ? WHERE task_id = ? AND user_id = ?',
                (new_description, task_id, user_id)
            )

        if new_difficulty:
            cursor.execute(
                'UPDATE tasks SET difficulty = ? WHERE task_id = ? AND user_id = ?',
                (new_difficulty, task_id, user_id)
            )

        if new_deadline:
            date_error = check_date_validation(new_deadline)
            if date_error:
                error_message.text = date_error
                database.close()
                return

            deadline_date = datetime.strptime(new_deadline, "%d.%m.%Y").strftime("%d.%m.%Y")
            cursor.execute(
                'UPDATE tasks SET deadline = ? WHERE task_id = ? AND user_id = ?',
                (deadline_date, task_id, user_id)
            )

    commit_and_close(database)

    error_message.text = ""


def update_task_status(user_id, task_id):
    """
    Aktualisiert den Status einer Aufgabe und vergibt Erfahrungspunkte (XP).
    Bei jedem Statuswechsel wird die Datenbank aktualisiert.
    """

    database, cursor = get_database_cursor()

    cursor.execute('''SELECT status, difficulty FROM tasks WHERE task_id = ? AND user_id = ?''', (task_id, user_id))
    task = cursor.fetchone()
    new_status = ""

    if task:
        current_status, difficulty = task
        if current_status == 'Beendet':
            commit_and_close(database)
            return

        if current_status == 'Erstellt':
            new_status = 'In Bearbeitung'
        elif current_status == 'In Bearbeitung':
            new_status = 'Beendet'

            if difficulty.lower() == 'einfach':
                xp_gain = 1
            elif difficulty.lower() == 'normal':
                xp_gain = 2
            elif difficulty.lower() == 'schwer':
                xp_gain = 4
            else:
                xp_gain = 0

            update_user_xp_and_level(user_id, xp_gain)

        cursor.execute('UPDATE tasks SET status = ? WHERE task_id = ? AND user_id = ?', (new_status, task_id, user_id))
        commit_and_close(database)


def list_all_tasks(user_id):
    """
    Alle Aufgaben werden gefetched (auch abgeschlossene)
    """
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM tasks WHERE user_id = ?''', (user_id,))
    tasks = cursor.fetchall()
    database.close()

    if tasks:
        return [task for task in tasks]

    else:
        return []


def list_open_tasks(user_id):
    """
    Alle offenen Aufgaben werden gefetched
    """
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM tasks WHERE user_id = ? AND status != ?''', (user_id, 'Beendet'))
    tasks = cursor.fetchall()
    database.close()

    if tasks:
        return [task for task in tasks]
    else:
        return []


def list_finished_tasks(user_id):
    """
    Alle abgeschlossenen Aufgaben werden gefetched
    """
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM tasks WHERE user_id = ? AND status == ?''', (user_id, 'Beendet'))
    tasks = cursor.fetchall()
    database.close()

    if tasks:
        return [task for task in tasks]
    else:
        return []


def delete_all_tasks(user_id):
    """
    Funktion ermöglicht das Löschen aller offenen Aufgaben
    """
    database, cursor = get_database_cursor()
    cursor.execute('''DELETE FROM tasks WHERE user_id = ?''', (user_id,))
    commit_and_close(database)


def delete_task(user_id, task_id):
    """
    Funktion ermöglicht das Löschen einer bestimmten Aufgaben
    """
    database, cursor = get_database_cursor()

    cursor.execute('''SELECT * FROM tasks WHERE task_id = ? AND user_id = ?''', (task_id, user_id))
    task = cursor.fetchone()

    if task:
        cursor.execute('DELETE FROM tasks WHERE task_id = ? AND user_id = ?', (task_id, user_id))
        commit_and_close(database)
    else:
        ui.notify("Aufgabe nicht gefunden.")
