from database import get_database_cursor, commit_and_close

# Neue Aufgabe erstellen
def create_new_task(description, deadline, user_email):
    database, cursor = get_database_cursor()
    status = 'Erstellt'
    cursor.execute('''
          INSERT INTO tasks (description, status, deadline, user_email)
          VALUES (?, ?, ?, ?)
      ''', (description, status, deadline, user_email))

    commit_and_close(database)
    print(f"Aufgabe '{description}' erfolgreich erstellt.")

# Alle Aufgaben anzeigen
def list_all_tasks(user_email):
    database, cursor = get_database_cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_email = ?', (user_email,))
    tasks = cursor.fetchall()

    if tasks:
        print(f"{'ID':<5} | {'Beschreibung':<20} | {'Status':<10} | {'Fälligkeitsdatum':<10}")
        print("-" * 60)
        for task in tasks:
            print(f"{task[0]:<5} | {task[1]:<20} | {task[2]:<10} | {task[3]:<10}")
    else:
        print("Keine Aufgaben vorhanden.")

# Status einer Aufgabe aktualisieren
def update_task_status(task_id, new_status, user_email):
    database, cursor = get_database_cursor()
    cursor.execute('''
        UPDATE tasks
        SET status = ?
        WHERE id = ? AND user_email = ?
    ''', (new_status, task_id, user_email))

    commit_and_close(database)
    print(f"Aufgabe ID {task_id} erfolgreich auf '{new_status}' aktualisiert.")

# Aufgabe löschen
def delete_task(task_id, user_email):
    database, cursor = get_database_cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ? AND user_email = ?', (task_id, user_email))
    commit_and_close(database)
    print(f"Aufgabe ID {task_id} erfolgreich gelöscht.")

def delete_all_tasks(user_email):
    database, cursor = get_database_cursor()
    cursor.execute('DELETE FROM tasks WHERE user_email = ?', (user_email,))
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="tasks";')  # ID zurücksetzen
    commit_and_close(database)
    print("Alle Aufgaben wurden erfolgreich gelöscht.")

