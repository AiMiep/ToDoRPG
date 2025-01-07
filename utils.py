from datetime import datetime
from tasks import create_new_task, list_all_tasks, delete_task, delete_all_tasks, update_task_status, list_all_open_tasks, list_finished_tasks
from user import print_user_data, update_race_and_class

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
    print("\n=== Task-Manager ===")
    print("1. Neue Aufgabe hinzufügen")
    print("2. Status einer Aufgabe ändern")
    print("3. Offene Aufgaben anzeigen")
    print("4. Alle Aufgaben anzeigen")
    print("5. Abgeschlossene Aufgaben anzeigen")
    print("6. Eine Aufgabe löschen")
    print("7. Alle Aufgaben löschen")
    print("8. Benutzerinformationen anzeigen")
    print("9. Rasse und Klasse ändern")
    print("10. Beenden")
    print("====================")


def task_manager():
    global user_id
    while True:
        show_task_options()
        option = input("Wähle eine Option (1-10): ").strip()

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
            update_race_and_class(user_id)

        elif option == '10':
            print("Task-Manager wird beendet. Bis bald!")
            break

        else:
            print("Ungültige Eingabe. Bitte eine Zahl zwischen 1 und 10 wählen.")
