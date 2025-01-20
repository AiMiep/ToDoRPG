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
        'text-align: center; color: white; font-size: 3.5vw; font-weight: bold;').classes('w-full')

    ui.button(
        'START', color='black',
        on_click=lambda: check_user_and_redirect()
    ).style(
        'display: block; margin: 6.5vh auto; text-align: center; font-weight: bold;'
        'font-size: 3vw; padding: 2vh 5vw; border-radius: 2vh; color: white;'
    )

    ui.label('MADE BY THE BEST FROM THE BEST').style(
        'font-size: 1.5vw; color: white; font-weight: bold; font-style: italic;').classes('w-full absolute bottom-4')


def check_user_and_redirect():
    database, cursor = get_database_cursor()
    cursor.execute("SELECT COUNT(*) FROM users")

    if initialize_user():
        ui.run_javascript('window.location.href="/homepage"')
    else:
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
        }
    </style>
    """)

    ui.label('MENU').style('color: white; font-size: 7vw; font-weight: bold; margin: 2vh;')

    button_style = (
        'font-weight: bold; font-size: 2.5vw; border-radius: 2vh; color: black; '
        'width: 40%; padding: 2vh; display: block;'
    )

    ui.button('Aufgaben Funktionen', icon='checklist', color='rgba(255, 255, 255, 0.8)',
              on_click=lambda: ui.run_javascript("window.location.href = '/show_tasks';")
              ).style(button_style)

    ui.button('User Funktionen', icon='face', color='rgba(255, 255, 255, 0.8)',
              on_click=lambda: ui.run_javascript("window.location.href = '/user_functions';")
              ).style(button_style)

    ui.button('Beenden', icon='logout', color='rgba(255, 255, 255, 0.8)',
              on_click=lambda: ui.run_javascript("window.location.href = '/startpage';")
              ).style(button_style)