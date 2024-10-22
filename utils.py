from datetime import datetime
from tasks import create_new_task, list_all_tasks, update_task_status, delete_task, delete_all_tasks
from database import create_table

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

def task_manager():
    create_table()
    while True:
        show_task_options()
        try:
            option = input("Wähle eine Option (1-6): ")
        except KeyboardInterrupt:
            print("\nProgramm wird beendet...")
            break

        if option == '1':
            description = input("Beschreibung: ")
            deadline = get_valid_date()
            create_new_task(description, deadline)

        elif option == '2':
            list_all_tasks()

        elif option == '3':
            task_id = int(input("ID der zu aktualisierenden Aufgabe: "))
            new_status = input("Neuer Status: ")
            update_task_status(task_id, new_status)

        elif option == '4':
            task_id = int(input("ID der zu löschenden Aufgabe: "))
            delete_task(task_id)

        elif option == '5':
            delete_all_tasks()

        elif option == '6':
            print("Task-Manager beendet.")
            break

        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")