from database import create_table
from nicegui import ui
from gui.taskify_gui import show_startpage
from gui.user_creation_gui import user_creation_page
from gui.task_menu_gui import nicegui_create_new_task, show_tasks_page
from gui.user_gui import functions_page
import os
from nicegui import app

app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))


def main():
    create_table()
    show_startpage()

    ui.run()

main()
