from datetime import datetime
from nicegui import ui
from functools import partial
from tasks import create_new_task, get_valid_date, list_all_tasks, list_finished_tasks, list_all_open_tasks, \
    delete_all_tasks, delete_task, update_task_data, update_task_status

user_id = 1


@ui.page('/create_task')
def nicegui_create_new_task():
    ui.label('Neue Aufgabe erstellen').style('text-align: center; width: 100%; font-size: 32px; font-weight: bold;')

    description_input = ui.input(label="Beschreibung", placeholder="Beschreibe die Aufgabe...",
                                 validation={'Zu kurz': lambda value: len(value) >= 3}).classes('w-full')
    deadline_input = ui.input(label="Fälligkeitsdatum", placeholder="TT.MM.JJJJ").classes('w-full')
    difficulty_input = ui.select(label="Schwierigkeitsstufe", options=["Leicht", "Mittel", "Schwer"]).classes('w-full')

    current_date = datetime.today().strftime('%d.%m.%Y')
    current_date_input = ui.input(label="Aktuelles Datum", value=current_date).classes('w-full')
    current_date_input.disable()

    error_message = ui.label('').style('color: red; font-size: 14px;')  # Fehlernachricht
    success_message = ui.label('').style('color: green; font-size: 14px;')  # Erfolgsnachricht

    def on_create_task():
        description = description_input.value
        deadline = deadline_input.value
        difficulty = difficulty_input.value
        status = 'Erstellt'

        # Prüfung ob Beschreibung hinzugefügt wurde
        if not description:
            error_message.text = "Beschreibung fehlt!"
            success_message.text = ''
            return

        # Gültigkeitsprüfung des Datums
        date_error = get_valid_date(deadline)
        if date_error:
            error_message.text = date_error
            success_message.text = ''
            return

        # Prüfung ob Schwierigkeit ausgewählt wurde
        if not difficulty:
            error_message.text = "Schwierigkeit fehlt!"
            success_message.text = ''
            return

        # Wenn keine Fehler vorliegen, Aufgabe erstellen
        error_message.text = ''
        success_message.text = ''

        create_new_task(difficulty, description, status, current_date, deadline, user_id)

        success_message.text = 'Aufgabe erfolgreich erstellt!'

    ui.button("Neue Aufgabe erstellen", on_click=on_create_task).classes('w-full')


@ui.page('/show_tasks')
def show_tasks_page():
    ui.label('Aufgaben anzeigen').style('text-align: center; width: 100%; font-size: 32px; font-weight: bold;')

    with ui.tabs().classes('w-full') as tabs:
        open_tasks = ui.tab('Offene Aufgaben')
        all_tasks = ui.tab('Alle Aufgaben')
        finished_tasks = ui.tab('Abgeschlossene Aufgaben')

    with (ui.tab_panels(tabs, value=open_tasks).classes('w-full')):
        # Offene Aufgaben
        with ui.tab_panel(open_tasks):
            tasks = list_all_open_tasks(user_id)
            if tasks:
                # Spaltenüberschrift einmal anzeigen
                with ui.row().classes('w-full text-center border-b border-gray-200 p-2'):
                    ui.label("Schwierigkeit").classes('flex-1')
                    ui.label("Beschreibung").classes('flex-1')
                    ui.label("Erstellungsdatum").classes('flex-1')
                    ui.label("Deadline").classes('flex-1')
                    ui.label("Status").classes('flex-1')
                    ui.label("Aktionen").classes('flex-1')

                # Aufgaben anzeigen
                for task in tasks:
                    with ui.row().classes('w-full text-center border-b border-gray-200 p-2'):
                        ui.label(task[1]).classes('flex-1')  # Schwierigkeit
                        ui.label(task[2]).classes('flex-1')  # Beschreibung
                        ui.label(task[4]).classes('flex-1')  # Erstellungsdatum
                        ui.label(task[5]).classes('flex-1')  # Deadline
                        ui.label(task[3]).classes('flex-1')  # Status

                        # Buttons für Aktionen
                        with ui.row().classes('flex-1'):
                            with ui.dialog() as dialog, ui.card():
                                ui.label('Änderungen: ')
                                description_input = ui.input(label="Beschreibung").classes('w-full')
                                deadline_input = ui.input(label="Fälligkeitsdatum", placeholder="TT.MM.JJJJ").classes(
                                    'w-full')
                                difficulty_input = ui.select(label="Schwierigkeitsstufe",
                                                             options=["Leicht", "Mittel", "Schwer"]).classes('w-full')

                                current_date = datetime.today().strftime('%d.%m.%Y')
                                current_date_input = ui.input(label="Aktuelles Datum", value=current_date).classes(
                                    'w-full')
                                current_date_input.disable()

                                with ui.row():
                                    ui.button('Speichern',
                                              on_click=partial(update_task_data, user_id, task[0], description_input,
                                                               deadline_input, difficulty_input))
                                    ui.button('Abbrechen', on_click=dialog.close)

                            ui.button(icon='edit', on_click=dialog.open).classes('rounded hover:bg-blue-600')
                            ui.button(icon='update', on_click=partial(update_task_status, user_id, task[0])).classes(
                                'rounded hover:bg-red-600')
                            ui.button(icon='delete', on_click=partial(delete_task, user_id, task[0])).classes(
                                'rounded hover:bg-red-600')

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
