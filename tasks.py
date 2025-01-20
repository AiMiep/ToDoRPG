from datetime import datetime
from nicegui import ui
from database import get_database_cursor, commit_and_close
from user import update_user_xp_and_level


def get_valid_date(deadline):
    try:
        date_obj = datetime.strptime(deadline, "%d.%m.%Y").date()

        if date_obj < datetime.now().date():
            return "❌ Datum ist in der Vergangenheit!"
        return None
    except ValueError:
        return "❌ Da stimmt doch was mit dem Datum nicht..."


def create_new_task(difficulty, description, status, current_date, deadline, user_id):
    database, cursor = get_database_cursor()

    cursor.execute('''
          INSERT INTO tasks (difficulty, description, status, date, deadline, user_id) 
          VALUES (?, ?, ?, ?, ?, ?)
      ''', (difficulty, description, status, current_date, deadline, user_id))

    commit_and_close(database)


def update_task_data(user_id, task_id, description_input, deadline_input, difficulty_input):
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
            try:
                deadline_date = datetime.strptime(new_deadline, "%d.%m.%Y").date()
                cursor.execute(
                    'UPDATE tasks SET deadline = ? WHERE task_id = ? AND user_id = ?',
                    (deadline_date, task_id, user_id)
                )
            except ValueError:
                print(f"Ungültiges Datumsformat: {new_deadline}")

    commit_and_close(database)

    ui.run_javascript('location.href = "/show_tasks"')


def update_task_status(user_id, task_id):
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

            if difficulty.lower() == 'leicht':
                xp_gain = 0.5
            elif difficulty.lower() == 'mittel':
                xp_gain = 1
            elif difficulty.lower() == 'schwer':
                xp_gain = 1.5
            else:
                xp_gain = 0

            update_user_xp_and_level(user_id, xp_gain)

        cursor.execute('UPDATE tasks SET status = ? WHERE task_id = ? AND user_id = ?', (new_status, task_id, user_id))
        commit_and_close(database)

    ui.run_javascript('window.location.href = "/show_tasks";')


def get_task_status_counts(user_id):
    tasks = list_all_tasks(user_id)
    task_status_counts = {'Erstellt': 0, 'In Bearbeitung': 0, 'Beendet': 0}

    for task in tasks:
        status = task[3]
        if status in task_status_counts:
            task_status_counts[status] += 1

    return task_status_counts


def list_all_tasks(user_id):
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM tasks WHERE user_id = ?''', (user_id,))
    tasks = cursor.fetchall()
    database.close()

    if tasks:
        return [task for task in tasks]

    else:
        return []


def list_all_open_tasks(user_id):
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM tasks WHERE user_id = ? AND status != ?''', (user_id, 'Beendet'))
    tasks = cursor.fetchall()
    database.close()

    if tasks:
        return [task for task in tasks]
    else:
        return []


def list_finished_tasks(user_id):
    database, cursor = get_database_cursor()
    cursor.execute('''SELECT * FROM tasks WHERE user_id = ? AND status == ?''', (user_id, 'Beendet'))
    tasks = cursor.fetchall()
    database.close()

    if tasks:
        return [task for task in tasks]
    else:
        return []


def delete_all_tasks(user_id):
    confirmation = input("Sicher? (ja/nein): ").lower()
    if confirmation == 'ja':
        database, cursor = get_database_cursor()
        cursor.execute('''DELETE FROM tasks WHERE user_id = ?''', (user_id,))
        commit_and_close(database)
        print("Alle Aufgaben gelöscht.")
    else:
        print("Löschen abgebrochen.")


def delete_task(user_id, task_id):
    database, cursor = get_database_cursor()

    cursor.execute('''SELECT * FROM tasks WHERE task_id = ? AND user_id = ?''', (task_id, user_id))
    task = cursor.fetchone()

    if task:
        cursor.execute('DELETE FROM tasks WHERE task_id = ? AND user_id = ?', (task_id, user_id))
        commit_and_close(database)
        ui.notify("Aufgabe erfolgreich gelöscht.")
        ui.run_javascript("location.reload()")
    else:
        ui.notify("Aufgabe nicht gefunden.")
