from nicegui import ui

def show_main_menu():
    ui.label('Taskify').style('text-align: center; width: 100%; font-size: 32px; font-weight: bold;')
    ui.button('Neue Aufgabe erstellen',
              on_click=lambda: ui.run_javascript("window.location.href = '/create_task';")).classes('w-full')
    ui.button('Aufgaben anzeigen',
              on_click=lambda: ui.run_javascript("window.location.href = '/show_tasks';")).classes('w-full')

