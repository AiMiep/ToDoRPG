from datetime import datetime
from nicegui import ui
from functools import partial
from tasks import create_new_task, get_valid_date, list_all_tasks, list_finished_tasks, list_all_open_tasks, \
    delete_all_tasks, delete_task, update_task_data, update_task_status

user_id = 1


def create_menu():
    with ui.row().classes('w-full bg-gray-100 text-gray-800 p-4 justify-between items-center') \
            .style('border-bottom: 1px solid #d1d5db; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);'):

        with ui.row():
            ui.label('Taskify').classes('text-xl font-bold').style('color: #4B5563;')

        with ui.row():
            ui.button(icon='home', on_click=lambda: ui.run_javascript("location.href = '/homepage'")) \
                .classes('bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md') \
                .style('border: 1px solid #d1d5db; padding: 0.5rem; width: 3rem; height: 3rem; display: flex; justify-content: center; align-items: center;')

            ui.button(icon='list_alt', on_click=lambda: ui.run_javascript("location.href = '/show_tasks'")) \
                .classes('bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md') \
                .style(
                'border: 1px solid #d1d5db; padding: 0.5rem; width: 3rem; height: 3rem; display: flex; justify-content: center; align-items: center;')

            ui.button(icon='add', on_click=lambda: ui.run_javascript("location.href = '/create_task'")) \
                .classes('bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md') \
                .style(
                'border: 1px solid #d1d5db; padding: 0.5rem; width: 3rem; height: 3rem; display: flex; justify-content: center; align-items: center;')

            # Benutzereinstellungen-Button (Icon statt Text)
            ui.button(icon='person', on_click=lambda: ui.run_javascript("location.href = '/user_functions'")) \
                .classes('bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md') \
                .style(
                'border: 1px solid #d1d5db; padding: 0.5rem; width: 3rem; height: 3rem; display: flex; justify-content: center; align-items: center;')


@ui.page('/create_task')
def nicegui_create_new_task():
    create_menu()

    with ui.card().classes('w-full max-w-xl mx-auto p-4 shadow-lg'):
        description_input = ui.input(
            label="✏️ Was möchtest du tun?",
            placeholder="Beschreibe deine Aufgabe...",
            validation={'Das ist doch keine richtige Aufgabenbeschreibung!': lambda value: len(value) >= 3}
        ).classes('w-full')

        deadline_input = ui.input(label="📅 Fälligkeitsdatum", placeholder="TT.MM.JJJJ").classes('w-full mt-4')
        difficulty_input = ui.select(
            label="🎯 Wähle die Schwierigkeitsstufe deiner Aufgabe aus:",
            options=["Leicht", "Mittel", "Schwer"]
        ).classes('w-full mt-4')

        current_date = datetime.today().strftime('%d.%m.%Y')
        ui.input(
            label="📆 Aktuelles Datum:",
            value=current_date
        ).classes('w-full mt-4').disable()

        error_message = ui.label('').style('color: red; font-size: 14px; margin-top: 16px;')
        with ui.dialog() as dialog:
            with ui.card().style('animation: fadeIn 0.3s ease;').classes('p-6 shadow-md rounded-xl text-center'):
                ui.label('✅ Aufgabe wurde erfolgreich erstellt!').classes('text-lg font-bold mb-4')
                ui.button('Lets goo!', on_click=dialog.close).classes('bg-green-500 text-white px-4 py-2 rounded-lg mx-auto').style('display: block;')

        def on_create_task():
            description = description_input.value
            deadline = deadline_input.value
            difficulty = difficulty_input.value
            status = 'Erstellt'

            if not description:
                error_message.text = "❌ Aufgabenbeschreibung fehlt!"
                return

            date_error = get_valid_date(deadline)
            if date_error:
                error_message.text = date_error
                return

            if not difficulty:
                error_message.text = "❌ Schwierigkeitsstufe muss noch ausgewählt werden."
                return

            error_message.text = ''
            create_new_task(difficulty, description, status, current_date, deadline, user_id)
            dialog.open()

        ui.button(
            "➕ Aufgabe erstellen",
            on_click=on_create_task
        ).style('background-color: #4CAF50; color: white; padding: 10px; border-radius: 8px;').classes('w-full mt-4')


@ui.page('/show_tasks')
def show_tasks_page():
    create_menu()

    ui.label('Aufgaben anzeigen').style('text-align: center; width: 100%; font-size: 32px; font-weight: bold;')

    with ui.tabs().classes('w-full justify-center') as tabs:
        open_tasks = ui.tab('Offene Aufgaben').classes('flex-1 text-center')
        all_tasks = ui.tab('Alle Aufgaben').classes('flex-1 text-center')
        finished_tasks = ui.tab('Abgeschlossene Aufgaben').classes('flex-1 text-center')

    with ui.tab_panels(tabs, value=open_tasks).classes('w-full').style('min-height: 500px;'):

        # Offene Aufgaben
        with ui.tab_panel(open_tasks):
            tasks = list_all_open_tasks(user_id)
            if tasks:
                with ui.row().classes('w-full text-center border-b border-gray-200 p-2'):
                    ui.label("Schwierigkeit").classes('flex-1')
                    ui.label("Beschreibung").classes('flex-1')
                    ui.label("Erstellungsdatum").classes('flex-1')
                    ui.label("Deadline").classes('flex-1')
                    ui.label("Status").classes('flex-1')
                    ui.label("Aktionen").classes('flex-1')

                for task in tasks:
                    with ui.row().classes('w-full text-center border-b border-gray-200 p-2'):
                        ui.label(task[1]).classes('flex-1')  # Schwierigkeit
                        ui.label(task[2]).classes('flex-1')  # Beschreibung
                        ui.label(task[4]).classes('flex-1')  # Erstellungsdatum
                        ui.label(task[5]).classes('flex-1')  # Deadline
                        ui.label(task[3]).classes('flex-1')  # Status

                        with ui.row().classes('flex-2 justify-center gap-2'):
                            with ui.dialog() as dialog, ui.card():
                                ui.label('Änderungen: ')
                                description_input = ui.input(label="Beschreibung").classes('w-full')
                                deadline_input = ui.input(label="Fälligkeitsdatum", placeholder="TT.MM.JJJJ").classes('w-full')
                                difficulty_input = ui.select(label="Schwierigkeitsstufe", options=["Leicht", "Mittel", "Schwer"]).classes('w-full')

                                current_date = datetime.today().strftime('%d.%m.%Y')
                                current_date_input = ui.input(label="Aktuelles Datum", value=current_date).classes('w-full')
                                current_date_input.disable()

                                with ui.row():
                                    ui.button('Speichern',
                                              on_click=partial(update_task_data, user_id, task[0], description_input,
                                                               deadline_input, difficulty_input))
                                    ui.button('Abbrechen', on_click=dialog.close)

                            ui.button(icon='edit', on_click=dialog.open).classes('rounded hover:bg-blue-600')
                            ui.button(icon='update', on_click=partial(update_task_status, user_id, task[0])).classes('rounded hover:bg-green-600')
                            ui.button(icon='delete', on_click=partial(delete_task, user_id, task[0])).classes('rounded hover:bg-red-600')

            else:
                ui.label("Keine offene Aufgaben.").classes('w-full text-center').style(
                    'color: #777; font-style: italic;')

        # Alle Aufgaben
        with ui.tab_panel(all_tasks):
            tasks = list_all_tasks(user_id)
            if tasks:
                with ui.row().classes('w-full text-center border-b border-gray-200 p-2'):
                    ui.label("ID").classes('flex-1')
                    ui.label("Schwierigkeit").classes('flex-1')
                    ui.label("Beschreibung").classes('flex-1')
                    ui.label("Erstellungsdatum").classes('flex-1')
                    ui.label("Deadline").classes('flex-1')
                    ui.label("Status").classes('flex-1')

                for task in tasks:
                    task_status = task[3]
                    created_color = 'bg-red-100' if task_status.lower() == "erstellt" else ''
                    finished_color = 'bg-green-100' if task_status.lower() == "beendet" else ''

                    with ui.row().classes(
                            f'w-full text-center border-b border-gray-200 p-2 {created_color} {finished_color}'):
                        ui.label(task[0]).classes('flex-1')
                        ui.label(task[1]).classes('flex-1')
                        ui.label(task[2]).classes('flex-1')
                        ui.label(task[4]).classes('flex-1')
                        ui.label(task[5]).classes('flex-1')
                        ui.label(task[3]).classes('flex-1')

            else:
                ui.label("Keine Aufgaben.").classes('w-full text-center').style(
                    'color: #777; font-style: italic;')

        # Abgeschlossene Aufgaben
        with ui.tab_panel(finished_tasks):
            tasks = list_finished_tasks(user_id)
            if tasks:
                columns = [
                    {'name': 'task_id', 'label': 'ID', 'field': 'task_id'},
                    {'name': 'difficulty', 'label': 'Schwierigkeit', 'field': 'difficulty'},
                    {'name': 'description', 'label': 'Beschreibung', 'field': 'description'},
                    {'name': 'status', 'label': 'Status', 'field': 'status'},
                    {'name': 'current_date', 'label': 'Erstellungsdatum', 'field': 'current_date'},
                    {'name': 'deadline', 'label': 'Deadline', 'field': 'deadline'},
                ]

                rows = []
                for task in tasks:
                    row = {
                        'task_id': task[0],
                        'difficulty': task[1],
                        'description': task[2],
                        'status': task[3],
                        'current_date': task[4],
                        'deadline': task[5],
                    }
                    rows.append(row)

                ui.table(columns=columns, rows=rows).classes('w-full')
            else:
                ui.label("Keine abgeschlossenen Aufgaben.").classes('w-full text-center').style(
                    'color: #777; font-style: italic;')
