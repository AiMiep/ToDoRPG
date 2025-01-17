from database import create_table
from nicegui import ui
from gui.taskify_gui import show_main_menu
from gui.user_creation_gui import user_creation_page
from gui.task_menu_gui import nicegui_create_new_task, show_tasks_page
from gui.user_gui import functions_page  # Funktionen-Seite importieren
from user import initialize_user
import os
from nicegui import app

# Statische Dateien bereitstellen
app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))


def main():
    # Datenbank initialisieren
    create_table()

    # Seiten registrieren
    user_creation_page()
    nicegui_create_new_task()
    show_tasks_page()
    functions_page()  # Funktionen-Seite registrieren (aus extra_functions_gui.py)

    # Dynamische Weiterleitung auf Root-Seite
    @ui.page('/')
    def root_page():
        # Überprüfen, ob Benutzer existiert
        if initialize_user():
            # Benutzer existiert: Hauptmenü laden
            ui.run_javascript('window.location.href="/main_menu"')
        else:
            # Kein Benutzer vorhanden: Benutzererstellung laden
            ui.run_javascript('window.location.href="/create_user"')

    # Hauptmenü-Seite
    @ui.page('/main_menu')
    def main_menu_page():
        """
        Zeigt das Hauptmenü mit Navigation zu den verschiedenen Bereichen.
        """
        show_main_menu()
        ui.button('User Funktionen', on_click=lambda: ui.run_javascript("window.location.href='/functions';")).classes('w-full')

    # NiceGUI starten
    ui.run()


# Multiprocessing-kompatibler Einstiegspunkt
if __name__ in {"__main__", "__mp_main__"}:
    main()
