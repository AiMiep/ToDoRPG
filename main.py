from database import create_table
from nicegui import ui
from gui.taskify_gui import show_startpage
import gui.user_creation_gui
import gui.task_menu_gui
import gui.user_gui
import os
from nicegui import app

app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))

def main():
    create_table()
    show_startpage()

    ui.run()

main()
