from datetime import datetime
from nicegui import ui
from functools import partial
from tasks import create_new_task, get_valid_date, list_all_tasks, list_finished_tasks, list_all_open_tasks, \
    delete_all_tasks, delete_task, update_task_data, update_task_status

user_id = 1


def navbar_gui():
    with ui.row().style(
            'padding: 18px; '
            'display: flex; justify-content: space-between; align-items: center; '
            'border-bottom: 4px double white;'
    ).classes('w-full'):
        with ui.row().style('display: flex; margin-left: 20px;'):
            ui.button('Zurück zum Menü', icon='home', color='black',
                      on_click=lambda: ui.run_javascript("location.href = '/homepage'")
                      ).style('color: white; padding: 10px 20px; font-size: 16px; font-weight: bold;'
                              'border-radius: 30px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);')

        with ui.row():
            ui.label('Heute schon was erledigt?').style(
                'font-size: 2vw; font-weight: bold; text-align: center; color: white')

        # Rechter Bereich: Neue Aufgabe erstellen-Button
        with ui.row().style('display: flex; margin-right: 20px;'):
            ui.button('Neue Aufgabe erstellen', icon='add', color='black',
                      on_click=lambda: ui.run_javascript("location.href = '/create_task'")
                      ).style('color: white; padding: 10px 20px; font-size: 16px; font-weight: bold; '
                              'border-radius: 130px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);')


def navbar_add_task_gui():
    with ui.row().style(
            'padding: 18px; '
            'display: flex; justify-content: space-between; align-items: center; '
            'border-bottom: 4px double white;'
    ).classes('w-full'):
        with ui.row().style('display: flex; margin-left: 20px;'):
            ui.button('Zurück zur Aufgabenübersicht', icon='list_alt', color='black',
                      on_click=lambda: ui.run_javascript("location.href = '/show_tasks'")
                      ).style('color: white; padding: 10px 20px; font-size: 16px; font-weight: bold; '
                              'border-radius: 130px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);')

        with ui.row().style('display: flex; margin-right: 20px;'):
            ui.button('Weiter zum Menü', icon='home', color='black',
                      on_click=lambda: ui.run_javascript("location.href = '/homepage'")
                      ).style('color: white; padding: 10px 20px; font-size: 16px; font-weight: bold;'
                              'border-radius: 30px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);')


@ui.page('/create_task')
def nicegui_create_new_task():
    navbar_add_task_gui()

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
                ui.button('Lets goo!', on_click=dialog.close).classes(
                    'bg-green-500 text-white px-4 py-2 rounded-lg mx-auto').style('display: block;')

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
def show_tasks_gui():
    ui.add_head_html("""
    <style>
        body {
            background-image: url('images/fish.gif');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            margin: 0;
            font-family: "Courier New", Courier, monospace;
            overflow: hidden;
        }
    </style>
    """)

    navbar_gui()

    with ui.tabs().classes('w-full').style('color: white; font-size: 30px;') as tabs:
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
                        'padding: 1.5vh; background-color: rgba(0, 0, 0, 0.9); border: 3px solid black; color: white; font-weight: bold; font-size: 1.2vw; border-radius: 15px'):
                    ui.label("Schwierigkeit").classes('flex-1')
                    ui.label("Beschreibung").classes('flex-1')
                    ui.label("Erstellungsdatum").classes('flex-1')
                    ui.label("Deadline").classes('flex-1')
                    ui.label("Status").classes('flex-1')
                    ui.label("Aktionen").classes('flex-1')

                for task in tasks:
                    with ui.row().classes('w-full text-center p-4').style(
                            'border: 4px solid white; border-radius: 15px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); '
                            'background-color: rgba(255, 255, 255, 0.9); '
                            'display: flex; align-items: center; justify-content: center;'):
                        ui.label(task[1]).classes('flex-1')  # Schwierigkeit
                        ui.label(task[2]).classes('flex-1')  # Beschreibung
                        ui.label(task[4]).classes('flex-1')  # Erstellungsdatum
                        ui.label(task[5]).classes('flex-1')  # Deadline
                        ui.label(task[3]).classes('flex-1')  # Status

                        with ui.row().classes('flex-1 justify-center gap-2'):
                            with ui.dialog() as dialog_edit, ui.card().style('width: 50%'):
                                ui.label('Datenänderungen:').style(
                                    'font-size: 3vh; text-align: center; font-weight: bold;').classes('w-full')
                                description_input = ui.input(label="Neue Beschreibung").classes('w-full')
                                deadline_input = ui.input(label="Neues Fälligkeitsdatum",
                                                          placeholder="TT.MM.JJJJ").classes(
                                    'w-full')
                                difficulty_input = ui.select(label="Neue Schwierigkeitsstufe",
                                                             options=["Leicht", "Mittel", "Schwer"]).classes('w-full')

                                current_date = datetime.today().strftime('%d.%m.%Y')
                                current_date_input = ui.input(label="Aktuelles Datum", value=current_date).classes(
                                    'w-full')
                                current_date_input.disable()

                                with ui.row().classes('w-full justify-center gap-10'):
                                    ui.button('Speichern',
                                              on_click=partial(update_task_data, user_id, task[0], description_input,
                                                               deadline_input, difficulty_input))
                                    ui.button('Abbrechen', on_click=dialog_edit.close)

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
                        'padding: 1.5vh; background-color: rgba(0, 0, 0, 0.9); border: 3px solid black; color: white; font-weight: bold; font-size: 1.2vw; border-radius: 15px'):
                    ui.label("ID").classes('flex-1')
                    ui.label("Schwierigkeit").classes('flex-1')
                    ui.label("Beschreibung").classes('flex-1')
                    ui.label("Erstellungsdatum").classes('flex-1')
                    ui.label("Deadline").classes('flex-1')
                    ui.label("Status").classes('flex-1')

                for task in tasks:
                    task_status = task[3]
                    created_color = 'bg-red-100' if task_status.lower() == "erstellt" else ''
                    started_color = 'bg-blue-100' if task_status.lower() == "in bearbeitung" else ''
                    finished_color = 'bg-green-100' if task_status.lower() == "beendet" else ''

                    with ui.row().style('padding: 1.5vh; border-radius: 15px;').classes(
                            f'w-full text-center border-b border-gray-200 p-2 {created_color} {started_color} {finished_color}'):
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
                        'padding: 1.5vh; background-color: rgba(0, 0, 0, 0.9); border: 3px solid black; color: white; font-weight: bold; font-size: 1.2vw; border-radius: 15px'):
                    ui.label("ID").classes('flex-1')
                    ui.label("Schwierigkeit").classes('flex-1')
                    ui.label("Beschreibung").classes('flex-1')
                    ui.label("Erstellungsdatum").classes('flex-1')
                    ui.label("Deadline").classes('flex-1')

                for task in tasks:
                    with ui.row().style('padding: 1.5vh; background-color: rgba(255, 255, 255, 0.9); border-radius: 15px;').classes(
                            f'w-full text-center border-b border-gray-200 p-2'):
                        ui.label(task[0]).classes('flex-1')
                        ui.label(task[1]).classes('flex-1')
                        ui.label(task[2]).classes('flex-1')
                        ui.label(task[4]).classes('flex-1')
                        ui.label(task[5]).classes('flex-1')

            else:
                ui.label("Keine beendeten Aufgaben.").classes('w-full text-center').style(
                    'color: #777; font-style: italic;')