import os
from nicegui import ui, app
from user import create_new_user

# Statische Dateien bereitstellen
app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))


def fetch_avatars():
    """Lädt alle verfügbaren Avatare mit Beschreibung."""
    return [
        {'id': 1, 'name': 'Bäcker/in', 'description': 'Meister des Teigs!', 'path': 'avatars/baker.png'},
        {'id': 2, 'name': 'Maler/in', 'description': 'Kreativ und voller Ideen!', 'path': 'avatars/painter.png'},
        {'id': 3, 'name': 'Zauberer/in', 'description': 'Beherrscht mächtige Magie.', 'path': 'avatars/witch.png'},
    ]


@ui.page('/create_user')
def user_creation_page():
    """Zeigt die Seite zur Benutzererstellung mit RPG-Elementen."""
    avatars = fetch_avatars()
    selected_avatar = {'id': None}

    def select_avatar(avatar_id):
        selected_avatar['id'] = avatar_id
        ui.notify(f'Du hast den Avatar {avatar_id} ausgewählt!')

    # Hintergrund-Bild
    with ui.column().classes('min-h-screen w-screen justify-start items-center') \
            .style('background-image: url("/images/background.png"); background-size: cover; background-position: center;'):
        # Zentraler Kasten
        with ui.card().classes('bg-gray-100 bg-opacity-80 shadow-lg border-black border rounded-lg w-11/12 sm:w-3/4 md:w-2/3 p-8 mt-6'):
            # Titel und Beschreibung
            ui.label('Charaktererstellung').classes('text-2xl sm:text-3xl font-bold text-black text-center mt-4')
            ui.label('Gestalte deinen Helden und wähle deinen Avatar!').classes('text-sm text-gray-700 text-center mb-6')

            # Eingabefelder und Avatare nebeneinander
            with ui.row().classes('justify-between items-start w-full gap-8 flex-wrap'):
                # Linke Spalte: Eingaben
                with ui.column().classes('w-full md:w-1/2 items-center gap-4'):
                    ui.label('Dein Heldname').classes('text-lg font-bold text-black text-center')
                    username = ui.input(placeholder='z. B. Ragnar').classes('w-full text-sm')

                    ui.label('Wähle eine Rasse').classes('text-lg font-bold text-black text-center mt-4')
                    rasse = ui.radio(['Bäcker/in', 'Maler/in', 'Zauberer/in'], value='Bäcker/in').classes('text-sm')

                    ui.label('Wähle eine Klasse').classes('text-lg font-bold text-black text-center mt-4')
                    klasse = ui.radio(['Anfänger', 'Fortgeschritten', 'Profi'], value='Anfänger').classes('text-sm')

                # Rechte Spalte: Avatare
                with ui.row().classes('w-full md:w-1/2 justify-center flex-wrap gap-4'):
                    for avatar in avatars:
                        with ui.column().classes('items-center'):
                            ui.image(f'/images/{avatar["path"]}').classes(
                                'w-24 h-24 object-contain rounded-full border border-gray-300 shadow-sm'
                            )  # Avatar-Bild
                            ui.label(avatar['name']).classes('text-center font-bold text-gray-700 text-sm mt-2')
                            ui.label(avatar['description']).classes('text-center text-gray-500 text-xs')
                            ui.button('Auswählen', on_click=lambda a_id=avatar['id']: select_avatar(a_id)).classes(
                                'mt-2 w-full bg-blue-500 text-white text-xs rounded-md hover:bg-blue-600'
                            )

            # Fortschrittsleiste und Abenteuerstart
            with ui.column().classes('items-center w-full gap-4 mt-6'):
                progress = ui.linear_progress(0).classes('w-3/4')
                ui.button('Abenteuer starten!', on_click=lambda: create_user_action(username, rasse, klasse, selected_avatar, progress)).classes(
                    'w-1/3 bg-gradient-to-r from-blue-500 to-purple-600 text-white text-sm font-bold py-3 rounded-lg hover:shadow-lg'
                )

    # Benutzer erstellen und Abenteuer starten
    def create_user_action(username, rasse, klasse, selected_avatar, progress):
        """Erstellt einen neuen Benutzer und leitet weiter."""
        if not username.value or not rasse.value or not klasse.value or not selected_avatar['id']:
            ui.notify('Bitte alle Felder ausfüllen und einen Avatar auswählen!', color='negative')
            return

        create_new_user(username.value, rasse.value, klasse.value, selected_avatar['id'])
        ui.notify(f'Willkommen, {username.value}! Dein Abenteuer beginnt!', color='positive')

        # Fortschrittsbalken aktualisieren und weiterleiten
        progress.set_value(1)
        ui.timer(1, lambda: ui.run_javascript('window.location.href="/user_functions"'))
