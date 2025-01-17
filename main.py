from database import create_table
from gui.taskify_gui import show_main_menu
from nicegui import ui
import gui.task_menu_gui
from user import initialize_user


def main():
    create_table()
    initialize_user()
    show_main_menu()
    ui.run()

main()
