from nicegui import ui

from tasks import get_task_status_counts

user_id = 1

def show_main_menu():

    ui.label('Taskify').style('text-align: center; width: 100%; font-size: 32px; font-weight: bold;')

    ui.highchart({
        'title': {'text': 'Status-Statisik'},
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['Erstellt', 'In Bearbeitung', 'Beendet']},
        'yAxis': {'title': {'text': 'Anzahl der Aufgaben'}},
        'series': [
            {'name': 'Aufgaben',
             'data': [get_task_status_counts(user_id)['Erstellt'], get_task_status_counts(user_id)['In Bearbeitung'],
                      get_task_status_counts(user_id)['Beendet']]},
        ],
    }).classes('w-full h-60')

    ui.button('Neue Aufgabe erstellen',
              on_click=lambda: ui.run_javascript("window.location.href = '/create_task';")).classes('w-full')
    ui.button('Aufgaben anzeigen',
              on_click=lambda: ui.run_javascript("window.location.href = '/show_tasks';")).classes('w-full')

