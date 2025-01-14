from nicegui import ui, app
from database import create_table
from tasks import create_new_task, list_all_tasks, update_task_status, delete_task, delete_all_tasks, list_all_open_tasks, list_finished_tasks
from user import check_if_user_exists, create_new_user, update_avatar, update_race_and_class, print_user_data
import os
from nicegui import ui
from database import get_database_cursor, commit_and_close
from datetime import datetime
from user import get_all_avatars

# Statische Dateien bereitstellen
app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))

# Hauptcontainer für dynamischen Inhalt
content_container = ui.column().classes('w-full items-center')


def fetch_avatars():
    return [
        {'id': 1, 'name': 'Bäcker/in', 'path': 'avatars/baker.png'},
        {'id': 2, 'name': 'Maler/in', 'path': 'avatars/painter.png'},
        {'id': 3, 'name': 'Zauberer/in', 'path': 'avatars/witch.png'}
    ]


def show_user_creation_dialog():
    with ui.dialog() as dialog, ui.card():
        ui.label('Kein Benutzer gefunden. Bitte erstelle einen neuen Benutzer:').classes('text-bold')
        username = ui.input(label='Benutzername').classes('w-full')
        rasse = ui.select(['Bäcker/in', 'Maler/in', 'Zauberer/in'], label='Wähle eine Rasse').classes('w-full')
        klasse = ui.select(['Anfänger', 'Fortgeschritten', 'Profi'], label='Wähle eine Klasse').classes('w-full')

        avatars = fetch_avatars()
        selected_avatar = {'id': None}

        def select_avatar(avatar_id):
            selected_avatar['id'] = avatar_id
            ui.notify(f'Avatar {avatar_id} ausgewählt!')

        ui.label('Wähle einen Avatar:').classes('text-bold mt-4')
        with ui.row().classes('wrap'):
            for avatar in avatars:
                with ui.column().classes('items-center'):
                    ui.image(f'/images/{avatar["path"]}').classes('w-24 h-24 rounded-md')
                    ui.button(avatar['name'], on_click=lambda a_id=avatar['id']: select_avatar(a_id))

        def create_user_action():
            if not username.value or not rasse.value or not klasse.value or not selected_avatar['id']:
                ui.notify('Bitte alle Felder ausfüllen und einen Avatar auswählen!', color='negative')
                return
            create_new_user(username.value, rasse.value, klasse.value, selected_avatar['id'])
            ui.notify(f'Benutzer {username.value} erstellt!', color='positive')
            dialog.close()
            show_main_menu()

        ui.button('Benutzer erstellen', on_click=create_user_action).classes('mt-4 w-full')
        dialog.open()


def start_task_manager():
    create_table()
    if not check_if_user_exists():
        show_user_creation_dialog()
    else:
        show_main_menu()
    ui.run(title="ToDoRPG", reload=True)


def show_main_menu():
    print("DEBUG: show_main_menu wurde aufgerufen.")  # Debug-Ausgabe

    # Entferne vorhandene Inhalte und baue das Hauptmenü neu auf
    content_container.clear()

    with content_container:  # Inhalte innerhalb des Containers hinzufügen
        ui.label('Task Manager Menü').classes('text-2xl text-bold mb-4')
        ui.button('1. Neue Aufgabe hinzufügen', on_click=show_task_creation_dialog).classes('w-full')
        ui.button('2. Status einer Aufgabe ändern', on_click=show_task_status_dialog).classes('w-full')
        ui.button('3. Offene Aufgaben anzeigen', on_click=show_open_tasks).classes('w-full')
        ui.button('4. Alle Aufgaben anzeigen', on_click=show_all_tasks).classes('w-full')
        ui.button('5. Abgeschlossene Aufgaben anzeigen', on_click=show_finished_tasks).classes('w-full')
        ui.button('6. Eine Aufgabe löschen', on_click=show_task_deletion_dialog).classes('w-full')
        ui.button('7. Alle Aufgaben löschen', on_click=confirm_delete_all_tasks).classes('w-full')
        ui.button('8. Benutzerinformationen anzeigen', on_click=show_user_info).classes('w-full')
        ui.button('9. Rasse und Klasse ändern', on_click=show_race_class_change_dialog).classes('w-full')
        ui.button('10. Avatar ändern', on_click=show_avatar_change_dialog).classes('w-full')
        ui.button('11. Beenden', on_click=lambda: ui.notify('Programm beendet.')).classes('w-full')


def show_task_creation_dialog():
    with ui.dialog() as dialog, ui.card():
        description = ui.input(label='Beschreibung').classes('w-full')
        deadline = ui.input(label='Fälligkeitsdatum (TT.MM.JJJJ)').classes('w-full')
        difficulty = ui.select(['leicht', 'mittel', 'schwer'], label='Schwierigkeit').classes('w-full')

        def create_task():
            if not description.value or not deadline.value or not difficulty.value:
                ui.notify('Bitte alle Felder ausfüllen!', color='negative')
                return
            create_new_task(1, description.value, deadline.value, difficulty.value)
            ui.notify(f"Aufgabe '{description.value}' erstellt!", color='positive')
            dialog.close()

        ui.button('Aufgabe erstellen', on_click=create_task).classes('mt-4 w-full')
        ui.button('Abbrechen', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()


def show_task_status_dialog():
    tasks = list_all_open_tasks(1)
    with ui.dialog() as dialog, ui.card():
        if tasks:
            selected_task = ui.select({task[0]: task[1] for task in tasks}, label='Wähle eine Aufgabe').classes('w-full')

            def update_status():
                update_task_status(1, int(selected_task.value))
                ui.notify('Status geändert!', color='positive')
                dialog.close()

            ui.button('Status ändern', on_click=update_status).classes('mt-4 w-full')
        else:
            ui.label('Keine offenen Aufgaben gefunden.')
            ui.button('Schließen', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()


def show_open_tasks():
    tasks = list_all_open_tasks(1)
    with ui.dialog() as dialog, ui.card():
        if tasks:
            for task in tasks:
                ui.label(f"Aufgabe: {task[1]} - Status: {task[2]} - Deadline: {task[3]}")
        else:
            ui.label('Keine offenen Aufgaben gefunden.')
        ui.button('Schließen', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()


def show_all_tasks():
    tasks = list_all_tasks(1)
    with ui.dialog() as dialog, ui.card():
        if tasks:
            for task in tasks:
                ui.label(f"Aufgabe: {task[1]} - Status: {task[2]} - Deadline: {task[3]}")
        else:
            ui.label('Keine Aufgaben gefunden.')
        ui.button('Schließen', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()


def show_finished_tasks():
    tasks = list_finished_tasks(1)
    with ui.dialog() as dialog, ui.card():
        if tasks:
            for task in tasks:
                ui.label(f"Aufgabe: {task[1]} - Abgeschlossen am: {task[3]}")
        else:
            ui.label('Keine abgeschlossenen Aufgaben gefunden.')
        ui.button('Schließen', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()


def show_task_deletion_dialog():
    tasks = list_all_tasks(1)
    with ui.dialog() as dialog, ui.card():
        if tasks:
            selected_task = ui.select({task[0]: task[1] for task in tasks}, label='Wähle eine Aufgabe').classes('w-full')

            def delete_selected_task():
                delete_task(1, int(selected_task.value))
                ui.notify('Aufgabe gelöscht!', color='positive')
                dialog.close()

            ui.button('Löschen', on_click=delete_selected_task).classes('mt-4 w-full')
        else:
            ui.label('Keine Aufgaben gefunden.')
        ui.button('Schließen', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()


def confirm_delete_all_tasks():
    with ui.dialog() as dialog, ui.card():
        ui.label('Alle Aufgaben löschen?').classes('text-bold')
        ui.button('Ja', on_click=lambda: (delete_all_tasks(1), dialog.close(), ui.notify('Alle Aufgaben gelöscht!', color='positive'))).classes('mt-4 w-full')
        ui.button('Nein', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()


def show_user_info():
    user_info = print_user_data()
    with ui.dialog() as dialog, ui.card():
        if user_info:
            for user_id, info in user_info.items():
                ui.label(f"Benutzername: {info['username']} - Level: {info['level']} - XP: {info['xp']}")
        else:
            ui.label('Keine Benutzerinformationen gefunden.')
        ui.button('Schließen', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()


def show_race_class_change_dialog():
    with ui.dialog() as dialog, ui.card():
        rasse = ui.select(['Bäcker/in', 'Maler/in', 'Zauberer/in'], label='Neue Rasse').classes('w-full')
        klasse = ui.select(['Anfänger', 'Fortgeschritten', 'Profi'], label='Neue Klasse').classes('w-full')

        def update_race_and_class_action():
            update_race_and_class(1, rasse.value, klasse.value)
            ui.notify('Rasse und Klasse geändert!', color='positive')
            dialog.close()

        ui.button('Speichern', on_click=update_race_and_class_action).classes('mt-4 w-full')
        ui.button('Abbrechen', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()


def show_avatar_change_dialog():
    avatars = fetch_avatars()
    with ui.dialog() as dialog, ui.card():
        selected_avatar = {'id': None}

        def select_avatar(avatar_id):
            selected_avatar['id'] = avatar_id
            ui.notify(f'Avatar {avatar_id} ausgewählt!')

        for avatar in avatars:
            with ui.column().classes('items-center'):
                ui.image(f'/images/{avatar["path"]}').classes('w-24 h-24 rounded-md')
                ui.button(avatar['name'], on_click=lambda a_id=avatar['id']: select_avatar(a_id))

        def save_avatar():
            if selected_avatar['id']:
                update_avatar(1, selected_avatar['id'])
                ui.notify('Avatar geändert!', color='positive')
                dialog.close()
            else:
                ui.notify('Bitte einen Avatar auswählen!', color='negative')

        ui.button('Speichern', on_click=save_avatar).classes('mt-4 w-full')
        ui.button('Abbrechen', on_click=dialog.close).classes('mt-4 w-full')
        dialog.open()



def get_all_tasks(user_id):
    """
    Ruft alle Aufgaben für den angegebenen Benutzer aus der Datenbank ab.
    """
    database, cursor = get_database_cursor()
    cursor.execute('SELECT task_id, description, status, deadline FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    commit_and_close(database)
    return tasks


def get_valid_date():
    """
    Fragt ein gültiges Datum ab (Format: TT.MM.JJJJ) und gibt das Datum zurück.
    """
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


def create_user_gui():
    """
    GUI für die Erstellung eines neuen Benutzers.
    """
    with ui.dialog() as dialog, ui.card():
        ui.label('Benutzer erstellen').classes('text-bold')
        username = ui.input('Benutzername').classes('w-full')
        rasse = ui.select(['Bäcker/in', 'Maler/in', 'Zauberer/in'], label='Rasse').classes('w-full')
        klasse = ui.select(['Anfänger', 'Fortgeschritten', 'Profi'], label='Klasse').classes('w-full')

        avatars = get_all_avatars()
        selected_avatar = {'id': None}

        def select_avatar(avatar_id):
            selected_avatar['id'] = avatar_id
            ui.notify(f'Avatar {avatar_id} ausgewählt!')

        ui.label('Wähle einen Avatar:').classes('mt-4 text-bold')
        with ui.row().classes('wrap'):
            for avatar in avatars:
                if len(avatar) < 3 or not avatar[2]:
                    print(f"DEBUG - Fehlerhafter Avatar-Eintrag: {avatar}")
                    continue
                with ui.column().classes('items-center'):
                    ui.image(f'/{avatar[2]}').classes('w-32 h-32')
                    ui.button(f'{avatar[1]}', on_click=lambda a_id=avatar[0]: select_avatar(a_id))

        def create_user_action():
            if not selected_avatar['id']:
                ui.notify('Bitte einen Avatar auswählen!', color='negative')
                return
            # Hier die Benutzererstellung implementieren
            print(
                f"Benutzer {username.value}, Rasse {rasse.value}, Klasse {klasse.value}, Avatar {selected_avatar['id']} erstellt!"
            )
            dialog.close()

        ui.button('Erstellen', on_click=create_user_action)
        ui.button('Abbrechen', on_click=dialog.close)
        dialog.open()


def task_manager_gui():
    """
    GUI für den Task-Manager.
    """
    container = ui.column().classes('w-full items-center')  # Dynamischer Container für Ansichten

    def show_main_view():
        """
        Zeigt die Hauptansicht des Task-Managers.
        """
        container.clear()  # Inhalt des Containers löschen
        with container:
            ui.label('Aufgabenverwaltung').classes('text-2xl text-bold mb-4')

            ui.button('Neue Aufgabe hinzufügen', on_click=create_new_task_view).classes('w-full')
            ui.button('Alle Aufgaben anzeigen', on_click=list_all_tasks_view).classes('w-full')
            ui.button('Status einer Aufgabe ändern', on_click=update_task_status_view).classes('w-full')
            ui.button('Einzelne Aufgabe löschen', on_click=delete_task_view).classes('w-full')
            ui.button('Alle Aufgaben löschen', on_click=delete_all_tasks_view).classes('w-full')
            ui.button('Beenden', on_click=lambda: ui.notify("Task-Manager geschlossen.")).classes('w-full')

    def create_new_task_view():
        """
        Ansicht: Neue Aufgabe hinzufügen.
        """
        container.clear()
        with container:
            ui.label('Neue Aufgabe erstellen').classes('text-bold mb-4')
            description = ui.input('Beschreibung').classes('w-full')
            deadline = ui.input('Fälligkeitsdatum (TT.MM.JJJJ)').classes('w-full')
            difficulty = ui.select(['leicht', 'mittel', 'schwer'], label='Schwierigkeitsstufe').classes('w-full')

            def submit_task():
                # Hier sollte die Logik zum Hinzufügen zur Datenbank eingefügt werden
                ui.notify(f"Aufgabe '{description.value}' erstellt.")
                show_main_view()

            ui.button('Aufgabe erstellen', on_click=submit_task).classes('mt-4')
            ui.button('Zurück', on_click=show_main_view).classes('mt-4')

    def list_all_tasks_view():
        """
        Ansicht: Alle Aufgaben anzeigen.
        """
        container.clear()
        with container:
            tasks = get_all_tasks(1)  # Beispiel-User-ID
            if tasks:
                for task in tasks:
                    ui.label(f"Aufgabe {task[0]}: {task[1]}, Status: {task[2]}, Deadline: {task[3]}")
            else:
                ui.label('Keine Aufgaben gefunden.')
            ui.button('Zurück', on_click=show_main_view).classes('mt-4')

    def update_task_status_view():
        """
        Ansicht: Aufgabenstatus ändern.
        """
        container.clear()
        with container:
            tasks = get_all_tasks(1)  # Beispiel-User-ID
            if tasks:
                selected_task = ui.select(
                    {task[0]: f"{task[1]} (Status: {task[2]})" for task in tasks},
                    label='Wähle eine Aufgabe'
                ).classes('w-full')
                ui.button('Status ändern', on_click=lambda: ui.notify(f"Status für Aufgabe {selected_task.value} geändert.")).classes('mt-4')
            else:
                ui.label('Keine Aufgaben gefunden.')
            ui.button('Zurück', on_click=show_main_view).classes('mt-4')

    def delete_task_view():
        """
        Ansicht: Aufgabe löschen.
        """
        container.clear()
        with container:
            tasks = get_all_tasks(1)  # Beispiel-User-ID
            if tasks:
                selected_task = ui.select(
                    {task[0]: f"{task[1]} (Deadline: {task[3]})" for task in tasks},
                    label='Wähle eine Aufgabe zum Löschen'
                ).classes('w-full')

                def confirm_delete():
                    # Hier sollte die Logik zum Löschen aus der Datenbank eingefügt werden
                    ui.notify(f"Aufgabe '{selected_task.value}' gelöscht.")
                    delete_task_view()  # Aktualisierte Liste anzeigen

                ui.button('Aufgabe löschen', on_click=confirm_delete).classes('mt-4')
            else:
                ui.label('Keine Aufgaben gefunden.')
            ui.button('Zurück', on_click=show_main_view).classes('mt-4')

    def delete_all_tasks_view():
        """
        Ansicht: Alle Aufgaben löschen.
        """
        container.clear()
        with container:
            ui.label('Möchtest du wirklich alle Aufgaben löschen?').classes('text-bold')
            ui.button('Ja', on_click=lambda: (ui.notify("Alle Aufgaben gelöscht."), show_main_view())).classes('mt-4')
            ui.button('Nein', on_click=show_main_view).classes('mt-4')

    # Zeige die Hauptansicht
    show_main_view()
