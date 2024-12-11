from datetime import date, datetime
from database import get_database_cursor, commit_and_close

def create_new_task(user_id, description, deadline):
    database, cursor = get_database_cursor()
    status = 'Erstellt'
    current_date = date.today()

    cursor.execute('''
          INSERT INTO tasks (description, status, date, deadline, user_id) 
          VALUES (?, ?, ?, ?, ?)
      ''', (description, status, current_date, deadline, user_id))

    commit_and_close(database)
    print(f"Aufgabe '{description}' erfolgreich erstellt.")


# Alle Aufgaben anzeigen
def list_all_tasks(user_id):
    database, cursor = get_database_cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()

    if tasks:
        print(f"{'ID':<5} | {'Beschreibung':<20} | {'Status':<10} | {'Erstellungsdatum':<15} | {'Fälligkeitsdatum':<15}")
        print("-" * 100)
        for task in tasks:
            creation_date = datetime.strptime(task[3], "%Y-%m-%d").strftime("%d.%m.%Y")
            deadline = datetime.strptime(task[4], "%Y-%m-%d").strftime("%d.%m.%Y")
            print(f"{task[0]:<5} | {task[1]:<20} | {task[2]:<10} | {creation_date:<15} | {deadline:<15}")
    else:
        print("Keine Aufgaben vorhanden.")
