import os
from nicegui import ui, app
from database import get_database_cursor, commit_and_close
from user import update_user_avatar, select_user

# Globale Benutzer-ID (aktueller Benutzer)
user_id = 1

# Statische Dateien bereitstellen
app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))

@ui.page('/user_functions')
def functions_page():
    """
    Zeigt die zentrale Seite mit Dialogfenstern für Benutzeraktionen und Avatare.
    """
    # Hintergrundbild setzen
    with ui.column().classes('min-h-screen w-screen justify-start items-center') \
            .style('background-image: url("/images/background2.jpeg"); background-size: cover; background-position: center;'):
        # Weißer, halbtransparenter Kasten
        with ui.card().classes('rounded-xl shadow-2xl p-8 w-11/12 sm:w-3/4 md:w-2/3 mt-10').style(
                'background-color: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.3);'
        ):
            # Titel
            ui.label('🏰 Magische Taverne der Funktionen 🏰').classes(
                'text-4xl sm:text-5xl font-extrabold text-yellow-300 text-center mb-6'
            )

            # Beschreibung
            ui.label('Willkommen, Abenteurer! Wähle eine Funktion, um die magische Welt zu erkunden.').classes(
                'text-lg text-gray-700 text-center mb-8'
            )

            # Funktionen-Buttons
            with ui.column().classes('gap-4'):
                ui.button('🛡️ Benutzerstatus prüfen', on_click=show_user_status_dialog).classes(
                    'bg-gradient-to-r from-green-400 to-teal-500 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                )
                ui.button('📜 Alle Benutzer anzeigen', on_click=show_all_users_dialog).classes(
                    'bg-gradient-to-r from-purple-600 to-pink-500 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                )
                ui.button('🎒 Benutzer-Items anzeigen', on_click=show_user_items_dialog).classes(
                    'bg-gradient-to-r from-orange-400 to-red-500 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                )
                ui.button('✨ Neuen Benutzer erstellen',
                          on_click=lambda: ui.run_javascript('window.location.href="/create_user"')).classes(
                    'bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                )
                ui.button('🔄 Benutzer wechseln', on_click=show_switch_user_dialog).classes(
                    'bg-gradient-to-r from-gray-400 to-gray-600 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                )

            # Avatare anzeigen
            display_avatars()

            # Zurück zum Hauptmenü
            ui.button('🏠 Zurück zum Hauptmenü',
                      on_click=lambda: ui.run_javascript("window.location.href='/main_menu';")).classes(
                'bg-gray-600 text-white font-bold text-lg w-full rounded-lg py-3 mt-6 hover:shadow-xl')




def display_avatars():
    """
    Zeigt alle verfügbaren Avatare in einem Grid und ermöglicht das Ändern des Avatars.
    """
    database, cursor = get_database_cursor()
    cursor.execute('SELECT avatar_id, name, description, path FROM avatars')
    avatars = cursor.fetchall()
    commit_and_close(database)

    with ui.row().classes('justify-center flex-wrap gap-8 mt-6'):
        for avatar_id, name, description, path in avatars:
            with ui.column().classes('items-center gap-2'):
                # Avatar-Bild
                ui.image(f'/images/{path}').classes(
                    'w-24 h-24 object-contain rounded-full border border-gray-300 shadow-sm'
                )
                # Avatar-Name und Beschreibung
                ui.label(name).classes('text-center font-bold text-gray-700 text-sm')
                # Button: Avatar auswählen
                ui.button(
                    text='Auswählen',
                    on_click=lambda a_id=avatar_id: select_avatar(a_id)
                ).classes('mt-2 bg-blue-500 text-white text-xs rounded-md hover:bg-blue-600')

def select_avatar(avatar_id):
    """
    Speichert den ausgewählten Avatar für den aktuellen Benutzer.
    """
    global user_id
    update_user_avatar(user_id, avatar_id)
    ui.notify(f"Avatar erfolgreich geändert! Neuer Avatar-ID: {avatar_id}", color='positive')

def show_user_status_dialog():
    """
    Zeigt die Details des aktuellen Benutzers in einem Dialogfenster.
    """
    global user_id
    print(f"DEBUG: Benutzerstatus wird für Benutzer-ID {user_id} geladen.")  # Debugging

    database, cursor = get_database_cursor()
    cursor.execute(
        'SELECT username, rasse, klasse, path, level, xp FROM users u JOIN avatars a ON u.avatar_id = a.avatar_id WHERE user_id = ?',
        (user_id,))
    user = cursor.fetchone()
    commit_and_close(database)

    if user:
        username, rasse, klasse, avatar_path, level, xp = user
        print(f"DEBUG: Geladene Benutzerdaten: {user}")  # Debugging

        with ui.dialog() as dialog:
            with ui.card():
                ui.label(f'🔍 Benutzerstatus: {username}').classes('text-2xl font-bold text-center mb-4')
                ui.image(f'/images/{avatar_path}').classes('w-32 h-32 rounded-full mx-auto shadow-lg')
                ui.label(f'🏹 Rasse: {rasse}').classes('text-lg text-gray-700')
                ui.label(f'⚔️ Klasse: {klasse}').classes('text-lg text-gray-700')
                ui.label(f'⭐ Level: {level}').classes('text-lg text-gray-700')
                ui.label(f'💎 XP: {xp}').classes('text-lg text-gray-700')
                ui.button('Schließen', on_click=dialog.close).classes('mt-4 bg-blue-500 text-white rounded-lg')

            dialog.open()
    else:
        print("DEBUG: Kein Benutzer gefunden.")
        ui.notify("Kein Benutzer gefunden.", color='negative')

def show_all_users_dialog():
    """
    Zeigt alle Benutzer in einem Dialogfenster in einer Tabelle.
    """
    # Benutzer aus der Datenbank abrufen
    database, cursor = get_database_cursor()
    cursor.execute('SELECT username, rasse, klasse, path, level, xp FROM users u JOIN avatars a ON u.avatar_id = a.avatar_id')
    users = cursor.fetchall()
    commit_and_close(database)

    with ui.dialog() as dialog:
        with ui.card():
            # Titel
            ui.label('📜 Alle Benutzer').classes('text-2xl font-bold text-center mb-4')

            # Benutzerliste als benutzerdefinierte Tabelle anzeigen
            with ui.column().classes('w-full'):
                # Tabellenkopf
                with ui.row().classes('font-bold text-left bg-gray-100 py-2 px-4 rounded-t-lg'):
                    ui.label('Avatar').classes('w-1/6 text-center')  # Spalte für Avatar
                    ui.label('Name').classes('w-1/6')
                    ui.label('Rasse').classes('w-1/6')
                    ui.label('Klasse').classes('w-1/6')
                    ui.label('Level').classes('w-1/6')
                    ui.label('XP').classes('w-1/6')

                # Tabelleninhalt
                for username, rasse, klasse, avatar_path, level, xp in users:
                    with ui.row().classes('py-2 px-4 border-b border-gray-200 items-center'):
                        # Avatar anzeigen (klein)
                        ui.image(f'/images/{avatar_path}').classes('w-8 h-8 rounded-full shadow-sm').style('margin-right: 8px')
                        # Benutzerinformationen
                        ui.label(username).classes('w-1/6')
                        ui.label(rasse).classes('w-1/6')
                        ui.label(klasse).classes('w-1/6')
                        ui.label(str(level)).classes('w-1/6')
                        ui.label(str(xp)).classes('w-1/6')

            # Schließen-Button
            ui.button('Schließen', on_click=dialog.close).classes('mt-4 bg-blue-500 text-white rounded-lg')

        dialog.open()


def show_user_items_dialog():
    """
    Zeigt die Items des aktuellen Benutzers in einem Dialogfenster.
    """
    database, cursor = get_database_cursor()
    cursor.execute('''
        SELECT i.name, i.path
        FROM user_items ui
        JOIN items i ON ui.item_id = i.item_id
        WHERE ui.user_id = ?
    ''', (user_id,))
    items = cursor.fetchall()
    commit_and_close(database)

    with ui.dialog() as dialog:
        with ui.card():
            ui.label('🎒 Deine Items').classes('text-2xl font-bold text-center mb-4')
            if items:
                with ui.grid(columns=3).classes('gap-4'):
                    for name, path in items:
                        with ui.column().classes('items-center'):
                            ui.image(f'/images/{path}').classes('w-24 h-24 rounded-full shadow-lg')
                            ui.label(name).classes('text-sm text-gray-700')
            else:
                ui.label('Du hast noch keine Items gesammelt.').classes('text-gray-500 text-center')
            ui.button('Schließen', on_click=dialog.close).classes('mt-4 bg-red-500 text-white rounded-lg')

        dialog.open()

def show_switch_user_dialog():
    """
    Zeigt einen Dialog an, um den Benutzer zu wechseln.
    """
    database, cursor = get_database_cursor()
    cursor.execute('SELECT user_id, username, path FROM users u JOIN avatars a ON u.avatar_id = a.avatar_id')
    users = cursor.fetchall()
    commit_and_close(database)

    with ui.dialog() as dialog:
        with ui.card():
            ui.label('🔄 Benutzer wechseln').classes('text-2xl font-bold text-center mb-4')

            with ui.column().classes('gap-4'):
                for user_id_in_db, username, avatar_path in users:
                    with ui.row().classes('items-center gap-4'):
                        ui.image(f'/images/{avatar_path}').classes('w-12 h-12 rounded-full shadow-lg')
                        ui.label(username).classes('text-lg font-bold text-gray-700')
                        ui.button('Wechseln', on_click=lambda uid=user_id_in_db: handle_user_switch(uid, dialog)).classes(
                            'bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600'
                        )

            # Schließen-Button
            ui.button('Schließen', on_click=dialog.close).classes('mt-4 bg-gray-500 text-white rounded-lg')

        dialog.open()


def handle_user_switch(selected_user_id, dialog):
    """
    Wechselt den Benutzer und schließt den Dialog.
    """
    global user_id
    user_id = selected_user_id  # Benutzer-ID aktualisieren
    print(f"DEBUG: Benutzer-ID nach Wechsel: {user_id}")  # Debugging

    dialog.close()  # Dialog schließen

    # Direkt den neuen Benutzerstatus anzeigen
    ui.notify(f"Benutzer erfolgreich gewechselt! Neue Benutzer-ID: {user_id}", color='positive')
    show_user_status_dialog()  # Neuer Benutzerstatus anzeigen

