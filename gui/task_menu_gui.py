from datetime import datetime
from nicegui import ui
from tasks import create_new_task, check_date_validation, list_all_tasks, list_finished_tasks, list_open_tasks, \
    delete_all_tasks, delete_task, edit_task_attributes, update_task_status

user_id = 1


def navigation_bar_gui():
    """
    Benutzer kann mithilfe der Navigationsleiste zum Hauptmenü zurückzukehren oder auch eine neue Aufgabe zu erstellen.
    """
    dialog = create_new_task_dialog()

    with ui.row().style(
            'padding: 18px; display: flex; justify-content: space-between; align-items: center; '
            'border-bottom: 4px double white;').classes('w-full'):
        with ui.row().style('display: flex; margin-left: 20px;'):
            ui.button('Zurück zum Menü', icon='home', color='rgba(0, 0, 0, 0.7)',
                      on_click=lambda: ui.run_javascript("location.href = '/homepage'")).style(
                'color: white; padding: 10px 20px; font-size: 2vh; font-weight: bold; border-radius: 130px;')

        with ui.row().style('display: flex; margin-right: 20px;'):
            ui.button('Neue Aufgabe erstellen', icon='add', color='rgba(0, 0, 0, 0.7)',
                      on_click=dialog.open).style(
                'color: white; padding: 10px 20px; font-size: 2vh; font-weight: bold; border-radius: 130px;')


def create_new_task_dialog():
    """
    In einem Dialog kann eine neue Aufgabe erstellt werden.
    Eingabe von Aufgabenbeschreibung, Fälligkeitsdatum und Schwierigkeitsstufe.
    """
    dialog = ui.dialog()
    with dialog:
        with ui.card().classes('w-full max-w-xl mx-auto p-4 shadow-lg').style('border-radius: 10px;'):
            ui.label('Aufgabenerstellung').style('font-size: 3vh; text-align: center; font-weight: bold;').classes(
                'w-full')

            description_input = ui.input(
                label="✏️ Was möchtest du tun?"
            ).classes('w-full')

            deadline_input = ui.input(label="📅 Fälligkeitsdatum", placeholder="TT.MM.JJJJ").classes('w-full')

            ui.label('🎯 Schwierigkeitsstufe').style('text-align:center;').classes('w-full mt-4')

            difficulty_input = ui.radio(
                options=["leicht", "normal", "schwer"],
                value="normal"
            ).props('inline').style('display: flex; justify-content: center; gap: 5%;').classes('w-full')

            current_date = datetime.today().strftime('%d.%m.%Y')
            ui.input(
                label="📆 Aktuelles Datum:",
                value=current_date
            ).classes('w-full mt-4').disable()

            error_message = ui.label('').style('color: red; font-size: 14px; margin-top: 16px;')

            def create_task_handler():
                """
                Prüfung, ob Eingaben gültig sind und erstellt dann die neue Aufgabe.
                Eingabefelder werden für die nächste Erstellung geleert.
                """
                description = description_input.value
                deadline = deadline_input.value
                difficulty = difficulty_input.value
                status = 'Erstellt'

                error = False

                if not description:
                    error_message.set_text("❌ Aufgabenbeschreibung fehlt!")
                    error = True

                date_error = check_date_validation(deadline)
                if date_error:
                    error_message.text = date_error
                    error = True

                if error:
                    return

                error_message.text = ''
                create_new_task(difficulty, description, status, current_date, deadline, user_id)
                dialog.close()
                reload_open_tasks_list.refresh()
                reload_finished_tasks_list.refresh()
                reload_all_tasks_list.refresh()

                description_input.set_value('')
                deadline_input.set_value('')

            with ui.row().classes('w-full justify-between items-center gap-4'):
                ui.button("Aufgabe erstellen", on_click=create_task_handler).classes('flex-1')
                ui.button("Abbrechen", on_click=dialog.close).classes('flex-1')

    return dialog


@ui.refreshable
def reload_open_tasks_list():
    """
    Aufgabenlisten können mithilfe der Annotation @ui.refreshable dynamisch aktualisiert werden,
    ohne die Seite neuladen zu müssen.
    """
    create_nicegui_elements_for_task_lists('open')


@ui.refreshable
def reload_finished_tasks_list():
    create_nicegui_elements_for_task_lists('finished')


@ui.refreshable
def reload_all_tasks_list():
    create_nicegui_elements_for_task_lists('all')


def update_task_status_and_refresh_list(user_id, task_id):
    """
    Status der Aufgabe wird um Stufe erhöht und die Listen aktualisiert.
    """
    update_task_status(user_id, task_id)
    reload_open_tasks_list.refresh()
    reload_all_tasks_list.refresh()
    reload_finished_tasks_list.refresh()


def delete_task_and_refresh_list(user_id, task_id):
    """
    Aufgabe wird gelöscht und die Listen aktualisiert.
    """
    delete_task(user_id, task_id)
    reload_open_tasks_list.refresh()
    reload_all_tasks_list.refresh()
    reload_finished_tasks_list.refresh()


def edit_task_attributes_and_refresh_list(user_id, task_id):
    """
    Daten der Aufgabe können angepasst werden.
    Nach dem Speichervorgang werden die Listen aktualisiert.
    """
    tasks = list_open_tasks(user_id)
    task = None

    for t in tasks:
        if t[0] == task_id:
            task = t
            break

    with ui.dialog() as dialog_edit:
        with ui.card().style('width: 50%'):
            ui.label('📝 Aufgabe bearbeiten').style(
                'font-size: 3vh; text-align: center; font-weight: bold;').classes('w-full')

            description_input = ui.input(label="Neue Beschreibung", value=task[2]).classes('w-full')

            deadline_input = ui.input(label="Neues Fälligkeitsdatum", placeholder="TT.MM.JJJJ", value=task[5]).classes(
                'w-full')

            ui.label('Neue Schwierigkeitsstufe').style('text-align:center;').classes('w-full mt-4')
            difficulty_input = ui.radio(
                options=["leicht", "normal", "schwer"],
                value=task[1]
            ).props('inline').style('display: flex; justify-content: center; gap: 5%;').classes('w-full')

            error_message = ui.label('').style('color: red; font-size: 14px; margin-top: 16px;')

            def save_edit():
                edit_task_attributes(user_id, task_id, description_input, deadline_input, difficulty_input,
                                     error_message)

                if not error_message.text:
                    dialog_edit.close()
                    reload_open_tasks_list.refresh()
                    reload_all_tasks_list.refresh()

            with ui.row().classes('w-full justify-center gap-10'):
                ui.button('✅ Speichern', on_click=save_edit).classes('w-1/3')
                ui.button('❌ Abbrechen', on_click=dialog_edit.close).classes('w-1/3')

    dialog_edit.open()


def create_nicegui_elements_for_task_lists(task_type):
    """
    Erstellt die einzelnen Nicegui/HTML Elemente.
    Buttons lösen die jeweiligen Aktionen aus.
    """
    if task_type == 'open':
        tasks = list_open_tasks(user_id)
    elif task_type == 'finished':
        tasks = list_finished_tasks(user_id)
    else:  # 'all'
        tasks = list_all_tasks(user_id)

    if tasks:
        with ui.row().classes('w-full text-center p-2').style(
                'padding: 1.5vh; background-color: rgba(0, 0, 0, 0.8); border: 3px solid black; color: white; '
                'font-weight: bold; font-size: 1.2vw; border-radius: 15px'):
            ui.label("Schwierigkeit").classes('flex-1')
            ui.label("Beschreibung").classes('flex-1')
            ui.label("Erstellungsdatum").classes('flex-1')
            ui.label("Deadline").classes('flex-1')
            ui.label("Status").classes('flex-1')

            if task_type == 'open':
                ui.label("Aktionen").classes('flex-1')

        for task in tasks:
            with ui.row().classes('w-full text-center p-2').style(
                    'font-size: 1vw; border: 3px solid white; border-radius: 15px; background-color: white;'
                    'display: flex; align-items: center; justify-content: center;'):
                ui.label(task[1]).classes('flex-1')  # Schwierigkeit
                ui.label(task[2]).classes('flex-1')  # Beschreibung
                ui.label(task[4]).classes('flex-1')  # Erstellungsdatum
                ui.label(task[5]).classes('flex-1')  # Deadline
                ui.label(task[3]).classes('flex-1')  # Status

                if task_type == 'open':
                    with ui.row().classes('flex-1 justify-center gap-2'):
                        ui.button(icon='update', color='#C8FACD',
                                  on_click=lambda task_id=task[0]: update_task_status_and_refresh_list(user_id,
                                                                                                       task_id)).classes(
                            'rounded').style('color: #34A853;')

                        ui.button(icon='edit', color='#AECBFA',
                                  on_click=lambda task_id=task[0]: edit_task_attributes_and_refresh_list(user_id,
                                                                                                         task_id)).classes(
                            'rounded').style('color: #1A73E8;')

                        ui.button(icon='delete', color='#FBCEDB',
                                  on_click=lambda task_id=task[0]: delete_task_and_refresh_list(user_id,
                                                                                                task_id)).classes(
                            'rounded').style('color: #EA4335;')

    else:
        ui.label(f"Keine {task_type} Aufgaben.").classes('w-full text-center').style('color: #777; font-style: italic;')


@ui.page('/show_tasks')
def display_tasks_gui():
    """
    Erstellt die Benutzeroberfläche zur Anzeige der Aufgaben.
    Enthält Navigation und Tabs für offene Aufgaben, alle Aufgaben und abgeschlossene Aufgaben.

    """

    ui.add_head_html("""
    <style>
        body {
            background-image: url('images/tasks_background.jpeg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            margin: 0;
            font-family: "Courier New", Courier, monospace;
        }
    </style>
    """)

    navigation_bar_gui()

    with ui.tabs().classes('w-full').style(
            'color: white; background-color: rgba(0, 0, 0, 0.7); padding: 10px;') as tabs:
        open_tasks = ui.tab('Offene Aufgaben').classes('flex-1')
        all_tasks = ui.tab('Alle Aufgaben').classes('flex-1')
        finished_tasks = ui.tab('Abgeschlossene Aufgaben').classes('flex-1')

    with ui.tab_panels(tabs, value=open_tasks).classes('w-full').style(
            'border-radius: 10px; background-color: transparent;'):
        with ui.tab_panel(open_tasks):
            reload_open_tasks_list()

        with ui.tab_panel(all_tasks):
            reload_all_tasks_list()

        with ui.tab_panel(finished_tasks):
            reload_finished_tasks_list()
