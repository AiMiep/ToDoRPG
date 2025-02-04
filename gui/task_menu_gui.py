from datetime import datetime
from nicegui import ui
from functools import partial
from tasks import create_new_task, get_valid_date, list_all_tasks, list_finished_tasks, list_all_open_tasks, \
    delete_all_tasks, delete_task, update_task_data, update_task_status

user_id = 1

def navbar_gui():
    with ui.dialog() as dialog:
        with ui.card().classes('w-full max-w-xl mx-auto p-4 shadow-lg').style('border-radius: 10px;'):

            ui.label('Aufgabenerstellung').style('font-size: 3vh; text-align: center; font-weight: bold;').classes(
                'w-full')

            description_input = ui.input(
                label="✏️ Was möchtest du tun?",
                validation={'Das ist doch keine richtige Aufgabenbeschreibung!': lambda value: len(value) >= 3}
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

            def on_create_task():
                description = description_input.value
                deadline = deadline_input.value
                difficulty = difficulty_input.value
                status = 'Erstellt'

                if not description:
                    error_message.set_text("❌ Aufgabenbeschreibung fehlt!")
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
                "Aufgabe erstellen",
                on_click=lambda: (on_create_task(), dialog.close(),
                                  ui.run_javascript("window.location.href = '/show_tasks';"))
            ).style('background-color: #4CAF50; color: white; padding: 10px; border-radius: 8px;').classes(
                'w-full mt-4')

    with ui.row().style(
            'padding: 18px; '
            'display: flex; justify-content: space-between; align-items: center; '
            'border-bottom: 4px double white;').classes('w-full'):

        with ui.row().style('display: flex; margin-left: 20px;'):
            ui.button('Zurück zum Menü', icon='home', color='rgba(0, 0, 0, 0.7)',
                      on_click=lambda: ui.run_javascript("location.href = '/homepage'")
                      ).style('color: white; padding: 10px 20px; font-size: 2vh; font-weight: bold; '
                              'border-radius: 130px;')

        with ui.row().style('display: flex; margin-right: 20px;'):
            ui.button('Neue Aufgabe erstellen', icon='add', color='rgba(0, 0, 0, 0.7)',
                      on_click=dialog.open).style(
                'color: white; padding: 10px 20px; font-size: 2vh; font-weight: bold; '
                'border-radius: 130px;')


@ui.refreshable
@ui.page('/show_tasks')
def show_tasks_gui():
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

    navbar_gui()

    with ui.tabs().classes('w-full').style(
            'color: white; background-color: rgba(0, 0, 0, 0.7); padding: 10px; border-radius: 130px;') as tabs:
        open_tasks = ui.tab('Offene Aufgaben').classes('flex-1')
        all_tasks = ui.tab('Alle Aufgaben').classes('flex-1')
        finished_tasks = ui.tab('Abgeschlossene Aufgaben').classes('flex-1')

    with ui.tab_panels(tabs, value=open_tasks).classes('w-full').style(
            'border-radius: 10px; background-color: transparent;'):
        # Offene Aufgaben
        with ui.tab_panel(open_tasks):
            tasks = list_all_open_tasks(user_id)
            if tasks:
                with ui.row().classes('w-full text-center p-2').style(
                        'padding: 1.5vh; background-color: rgba(0, 0, 0, 0.8); border: 3px solid black; color: white; '
                        'font-weight: bold; font-size: 1.2vw; border-radius: 15px'):
                    ui.label("Schwierigkeit").classes('flex-1')
                    ui.label("Beschreibung").classes('flex-1')
                    ui.label("Erstellungsdatum").classes('flex-1')
                    ui.label("Deadline").classes('flex-1')
                    ui.label("Status").classes('flex-1')
                    ui.label("Aktionen").classes('flex-1')

                for task in tasks:
                    with ui.row().classes('w-full text-center p-4').style(
                            'font-size: 1vw; border: 3px solid white; border-radius: 15px; color: black; backdrop-filter: blur(7.5px);'
                            'display: flex; align-items: center; justify-content: center;'):
                        ui.label(task[1]).classes('flex-1')  # Schwierigkeit
                        ui.label(task[2]).classes('flex-1')  # Beschreibung
                        ui.label(task[4]).classes('flex-1')  # Erstellungsdatum
                        ui.label(task[5]).classes('flex-1')  # Deadline
                        ui.label(task[3]).classes('flex-1')  # Status

                        with ui.row().classes('flex-1 justify-center gap-2'):
                            with ui.dialog() as dialog_edit, ui.card().style('width: 50%'):
                                ui.label('Datenänderung').style(
                                    'font-size: 3vh; text-align: center; font-weight: bold;').classes('w-full')

                                description_input = ui.input(label="Neue Beschreibung").classes('w-full')

                                deadline_input = ui.input(label="Neues Fälligkeitsdatum",
                                                          placeholder="TT.MM.JJJJ").classes('w-full')

                                ui.label('Neue Schwierigkeitsstufe').style('text-align:center;').classes('w-full mt-4')
                                difficulty_input = ui.radio(
                                    options=["leicht", "normal", "schwer"],
                                    value=task[1]
                                ).props('inline').style('display: flex; justify-content: center; gap: 5%;').classes(
                                    'w-full')

                                error_message = ui.label('').style('color: red; font-size: 14px; margin-top: 16px;')

                                with ui.row().classes('w-full justify-center gap-10'):
                                    ui.button('Speichern',
                                              on_click=partial(update_task_data, user_id, task[0], description_input,
                                                               deadline_input, difficulty_input, error_message))
                                    ui.button('Abbrechen',
                                              on_click=lambda: (dialog_edit.close(), error_message.set_text('')))

                            ui.button(icon='edit', color='#AECBFA', on_click=dialog_edit.open).classes('rounded').style(
                                'color: #1A73E8;')
                            ui.button(icon='update', color='#C8FACD',
                                      on_click=partial(update_task_status, user_id, task[0])).classes(
                                'rounded').style('color: #34A853;')

                            with ui.dialog() as dialog_delete, ui.card().style('width: 50%'):
                                ui.label('Willst du die Aufgabe wirklich löschen?').style(
                                    'font-size: 3vh; text-align: center; font-weight: bold;').classes('w-full')

                                with ui.row().classes('w-full justify-center gap-10'):
                                    ui.button('Ja',
                                              on_click=partial(delete_task, user_id, task[0]))
                                    ui.button('Nein', on_click=dialog_delete.close)

                            ui.button(icon='delete', color='#FBCEDB',
                                      on_click=dialog_delete.open).classes(
                                'rounded').style('color: #EA4335;')

            else:
                ui.label("Keine offene Aufgaben.").classes('w-full text-center').style(
                    'color: #777; font-style: italic;')

        # Alle Aufgaben
        with ui.tab_panel(all_tasks):
            tasks = list_all_tasks(user_id)
            if tasks:
                with ui.row().classes('w-full text-center p-2').style(
                        'padding: 1.5vh; background-color: rgba(0, 0, 0, 0.8); border: 3px solid black; color: white; '
                        'font-weight: bold; font-size: 1.2vw; border-radius: 15px'):
                    ui.label("ID").classes('flex-1')
                    ui.label("Schwierigkeit").classes('flex-1')
                    ui.label("Beschreibung").classes('flex-1')
                    ui.label("Erstellungsdatum").classes('flex-1')
                    ui.label("Deadline").classes('flex-1')
                    ui.label("Status").classes('flex-1')

                for task in tasks:
                    task_status = task[3].lower()

                    bg_color = (
                        'rgba(255, 230, 230, 0.8)' if task_status == "erstellt" else ''
                                                                                     'rgba(230, 243, 255, 0.8)' if task_status == "in bearbeitung" else ''
                                                                                                                                                        'rgba(230, 255, 235, 0.8)' if task_status == "beendet" else ''
                    )

                    border_color = (
                        'red' if task_status == "erstellt" else ''
                                                                'blue' if task_status == "in bearbeitung" else ''
                                                                                                               'green' if task_status == "beendet" else ''
                    )

                    with ui.row().style(
                            f'font-size: 1vw; background-color: {bg_color}; border-radius: 15px; color: black;'
                            f'display: flex; align-items: center; justify-content: center; border: 4px solid {border_color}; '
                    ).classes('w-full text-center p-2'):
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
                with ui.row().classes('w-full text-center p-2').style(
                        'padding: 1.5vh; background-color: rgba(0, 0, 0, 0.8); border: 3px solid black; color: white; '
                        'font-weight: bold; font-size: 1.2vw; border-radius: 15px'):
                    ui.label("ID").classes('flex-1')
                    ui.label("Schwierigkeit").classes('flex-1')
                    ui.label("Beschreibung").classes('flex-1')
                    ui.label("Erstellungsdatum").classes('flex-1')
                    ui.label("Deadline").classes('flex-1')

                for task in tasks:
                    with ui.row().style(
                            'font-size: 1vw; border: 4px solid black; border-radius: 15px; background-color: rgba(255, 255, 255, 0.8); color: black;'
                            'display: flex; align-items: center; justify-content: center;').classes(
                        f'w-full text-center border-b border-gray-200 p-2'):
                        ui.label(task[0]).classes('flex-1')
                        ui.label(task[1]).classes('flex-1')
                        ui.label(task[2]).classes('flex-1')
                        ui.label(task[4]).classes('flex-1')
                        ui.label(task[5]).classes('flex-1')

            else:
                ui.label("Keine beendeten Aufgaben.").classes('w-full text-center').style(
                    'color: #777; font-style: italic;')
