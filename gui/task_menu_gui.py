from datetime import datetime
from nicegui import ui
from functools import partial
from tasks import create_new_task, get_valid_date, list_all_tasks, list_finished_tasks, list_all_open_tasks, \
    delete_all_tasks, delete_task

user_id = 1

@ui.page('/create_task')
def nicegui_create_new_task():
    ui.label('Neue Aufgabe erstellen').style('text-align: center; width: 100%; font-size: 32px; font-weight: bold;')

    description_input = ui.input(label="Beschreibung", placeholder="Beschreibe die Aufgabe...").classes('w-full')
    deadline_input = ui.input(label="Fälligkeitsdatum (TT.MM.JJJJ)", placeholder="TT.MM.JJJJ").classes('w-full')
    difficulty_input = ui.select(label="Schwierigkeitsstufe", options=["Leicht", "Mittel", "Schwer"]).classes('w-full')

    error_message = ui.label('').style('color: red; font-size: 14px;')  # Fehlernachricht
    success_message = ui.label('').style('color: green; font-size: 14px;')  # Erfolgsnachricht

    def on_create_task():
        description = description_input.value
        deadline = deadline_input.value
        difficulty = difficulty_input.value
        status = 'Erstellt'
        current_date = datetime.today().strftime('%d.%m.%Y')

        # Prüfung ob Beschreibung hinzugefügt wurde
        if not description:
            error_message.text = "Beschreibung fehlt!."
            success_message.text = ''

        # Gültigkeitsprüfung des Datums
        date_error = get_valid_date(deadline)
        if date_error:
            error_message.text = date_error
            success_message.text = ''

        # Prüfung ob Schwierigkeit ausgewählt wurde
        if not difficulty:
            error_message.text = "Schwierigkeit fehlt!."
            success_message.text = ''

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

    with ui.tab_panels(tabs).classes('w-full'):
        # Offene Aufgaben
        with ui.tab_panel(open_tasks):
            tasks = list_all_open_tasks(user_id)
            if tasks:
                for task in tasks:
                    with ui.card().classes('shadow-lg bg-white rounded-lg w-full text-center'):
                        ui.label(f"Schwierigkeit: {task[1]}").classes('w-full text-center')
                        ui.label(f"Beschreibung: {task[2]}").classes('w-full text-center')
                        ui.label(f"Status: {task[3]}").classes('w-full text-center')
                        ui.label(f"Erstellungsdatum: {task[4]}").classes('w-full text-center')
                        ui.label(f"Deadline: {task[5]}").classes('w-full text-center')

                        task_id = task[0]

                        # Container für die Buttons nebeneinander und mittig
                        with ui.row().classes('w-full justify-center gap-4'):
                            # Löschen-Button mit 50% Breite
                            ui.button('Löschen', on_click=partial(delete_task, user_id, task_id)).classes(
                                'w-1/2 rounded-full hover:bg-red-600')

                            # Bearbeiten-Button mit 50% Breite
                            ui.button('Bearbeiten', on_click=partial(delete_task, user_id, task_id)).classes(
                                'w-1/2 rounded-full hover:bg-blue-600')

            else:
                ui.label("Keine offene Aufgaben.").classes('w-full text-center').style(
                    'color: #777; font-style: italic;')

        # Alle Aufgaben
        with ui.tab_panel(all_tasks):
            tasks = list_all_tasks(user_id)
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

                # Zeige die Tabelle an
                ui.table(columns=columns, rows=rows).classes('w-full')

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


def show_main_menu():
    ui.label('Task Manager Menü').style('text-align: center; width: 100%; font-size: 32px; font-weight: bold;')
    ui.button('Neue Aufgabe erstellen',
              on_click=lambda: ui.run_javascript("window.location.href = '/create_task';")).classes('w-full')
    ui.button('Aufgaben anzeigen',
              on_click=lambda: ui.run_javascript("window.location.href = '/show_tasks';")).classes('w-full')
