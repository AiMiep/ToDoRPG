from datetime import datetime
from tasks import create_new_task, list_all_tasks, delete_task, delete_all_tasks, update_task_status, list_all_open_tasks, list_finished_tasks
from user import print_user_data

user_id = 1

def get_valid_date():
    while True:
        deadline = input("Fälligkeitsdatum (TT.MM.JJJJ): ")
        try:
            date_obj = datetime.strptime(deadline, "%d.%m.%Y").date()
            if date_obj < datetime.now().date():
                print("Datum in der Vergangenheit.")
                continue
            return date_obj
        except ValueError:
            print("Ungültiges Datum. Bitte verwenden Sie das Format TT.MM.JJJJ.")

def show_task_options():
    print("\nTask-Manager")
    print("1. Hinzufügen neue Aufgabe")
    print("2. Änderung Status")
    print("3. Anzeige - Offene Aufgaben")
    print("4. Anzeige - Alle Aufgaben")
    print("5. Anzeige - Abgeschlossene Aufgaben")
    print("6. Löschung einer Aufgabe")
    print("7. Löschung aller Aufgaben")
    print("8. Userdaten anschauen")
    print("9. Beenden")

def task_manager():
    while True:
        show_task_options()
        option = input("Wähle eine Option (1-6): ")

        if option == '1':
            create_new_task(user_id)

        elif option == '2':
            list_all_open_tasks(user_id)
            update_task_status(user_id)

        elif option == '3':
            list_all_open_tasks(user_id)

        elif option == '4':
            list_all_tasks(user_id)

        elif option == '5':
            list_finished_tasks(user_id)

        elif option == '6':
            delete_task(user_id)

        elif option == '7':
            delete_all_tasks(user_id)

        elif option == '8':
            print_user_data()

        elif option == '9':
            print("Task-Manager beendet.")
            break

        else:
            print("Ungültige Eingabe.")
