from datetime import datetime
from tasks import create_new_task, list_all_tasks

user_id = 1

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
    print("3. Beenden")

def task_manager():
    while True:
        show_task_options()
        option = input("Wähle eine Option (1-3): ")

        if option == '1':
            description = input("Beschreibung: ")
            deadline = get_valid_date()
            create_new_task(user_id, description, deadline)

        elif option == '2':
            list_all_tasks(user_id)

        elif option == '3':
            print("Task-Manager beendet.")
            break

        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")