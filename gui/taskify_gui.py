from nicegui import ui
from database import get_database_cursor
from user import initialize_user

user_id = 1


@ui.page('/startpage')
def show_startpage():
    ui.add_head_html("""
    <style>
        body {
            background-image: url('images/kirby.gif');
            background-size: cover;
            background-position: center;
            margin: 0;
            font-family: "Courier New", Courier, monospace;
            overflow: hidden;
        }
    </style>
    """)

    ui.label('TASKIFY').style(
        'font-weight: bold; font-size: 8vw; color: white; text-align: center;'
    ).classes('w-full')

    ui.label('Get something done!').style(
        'text-align: center; color: white; font-size: 4.5vw; font-weight: bold;').classes('w-full')

    ui.button(
        'START', color='black',
        on_click=lambda: check_user_and_redirect()
    ).style(
        'display: block; margin: 7vh auto; text-align: center; font-weight: bold;'
        'font-size: 3vw; padding: 3vh 6vw; border-radius: 2vh; color: white;'
    )

    ui.label('MADE BY THE BEST FROM THE BEST').style(
        'font-size: 2vw; color: white; font-weight: bold; font-style: italic;').classes('w-full absolute bottom-4')


def check_user_and_redirect():
    database, cursor = get_database_cursor()
    cursor.execute("SELECT COUNT(*) FROM users")

    if initialize_user():
        # Benutzer existiert: Hauptmenü laden
        ui.run_javascript('window.location.href="/homepage"')
    else:
        # Kein Benutzer vorhanden: Benutzererstellung laden
        ui.run_javascript('window.location.href="/create_user"')


@ui.page('/homepage')
def show_main_menu():
    ui.add_head_html("""
    <style>
        body {
            background-image: url('images/mario.gif');
            background-size: cover;
            background-position: center;
            margin: 0;
            font-family: "Courier New", Courier, monospace;
            overflow: hidden;
        }
    </style>
    """)

    ui.label('MENU').style('color: white; font-size: 140px; font-weight: bold; margin: 50px;')

    button_style = 'font-weight: bold; font-size: 30px; border-radius: 10px; color: black; width: 40%; padding: 20px; margin-left: 50px'

    ui.button('Aufgaben Funktionen', icon='checklist', color='white',
              on_click=lambda: ui.run_javascript("window.location.href = '/show_tasks';")
              ).style(button_style)

    ui.button('User Funktionen', icon='face', color='white',
              on_click=lambda: ui.run_javascript("window.location.href = '/user_functions';")
              ).style(button_style)

    ui.button('Einstellungen', icon='settings', color='white',
              on_click=lambda: ui.run_javascript("window.location.href = '/error_page';")
              ).style(button_style)

    ui.button('Beenden', icon='logout', color='white',
              on_click=lambda: ui.run_javascript("window.location.href = '/startpage';")
              ).style(button_style)