import os
from nicegui import ui, app
from database import get_database_cursor, commit_and_close
from user import update_user_avatar, select_user, get_user_by_id, get_all_users

# Globale Benutzer-ID (aktueller Benutzer)
user_id = 1

# Statische Dateien bereitstellen
app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))

# Avatare für jede Kategorie
RACE_TO_AVATARS = {
    "Mensch (Mario Bros)": [
        {"id": 1, "name": "Held", "path": "newAvatars/M-Mario.jpg"},
        {"id": 2, "name": "Schurke", "path": "newAvatars/M-Wario.jpg"},
        {"id": 3, "name": "Prinzessin", "path": "newAvatars/M-Peach.jpg"}
    ],
    "Goronen/Zoras/Rito/Gerudo (Zelda)": [
        {"id": 7, "name": "Held", "path": "newAvatars/Z-Held.jpg"},
        {"id": 8, "name": "Bogenschütze", "path": "newAvatars/Z-Bogen.jpg"},
        {"id": 9, "name": "Gelehrter", "path": "newAvatars/Z-Gelehrter.jpg"}
    ],
    "Pokémon-Trainer (Pokémon)": [
        {"id": 4, "name": "Trainer", "path": "newAvatars/P-Trainer.jpg"},
        {"id": 5, "name": "Ranger", "path": "newAvatars/P-Ranger.jpg"},
        {"id": 6, "name": "Kampfkünstler", "path": "newAvatars/P-Brawler.jpg"}
    ]
}

def get_avatars_by_race(race):
    """Gibt die Avatare zurück, die zu einer bestimmten Rasse gehören."""
    return RACE_TO_AVATARS.get(race, [])

def get_avatar_path_by_id(avatar_id):
    """Gibt den Pfad eines Avatars basierend auf der ID zurück."""
    for race, avatars in RACE_TO_AVATARS.items():
        for avatar in avatars:
            if avatar["id"] == avatar_id:
                return f'/images/{avatar["path"]}'
    return None


@ui.page('/user_functions')
def functions_page():
    """Zentrale Seite für Benutzeraktionen, angepasst an die Rasse."""
    global user_id
    user = get_user_by_id(user_id)

    if not user:
        ui.notify('Kein Benutzer gefunden. Bitte erstellen Sie einen Benutzer.', color='negative')
        return

    username, rasse, klasse, avatar_id, level, xp = user
    avatars = get_avatars_by_race(rasse)

    with ui.column().classes('min-h-screen w-screen justify-start items-center').style(
        'background-image: url("/images/backgroundGif/DefaultBackgroundGif.gif"); background-size: cover; background-position: center;'):

        with ui.card().classes('rounded-xl shadow-2xl p-8 w-11/12 sm:w-3/4 md:w-2/3 mt-10').style(
            'background-color: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.3);'):

            ui.label('🏰 Willkommen! Schau dich um! 🏰').classes(
                'text-4xl sm:text-5xl font-extrabold text-yellow-300 text-center mb-6'
            ).style('font-family: "Courier New", Courier, monospace;')

            ui.label(f'Willkommen, {username}! Wähle eine Funktion aus.').classes(
                'text-lg text-gray-700 text-center mb-8'
            ).style('font-family: "Courier New", Courier, monospace;')

            # Benutzeraktionen
            with ui.column().classes('gap-4'):
                ui.button('🛡️ Benutzerstatus prüfen', on_click=show_user_status_dialog).classes(
                    'bg-gradient-to-r from-green-400 to-teal-500 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                ).style('font-family: "Courier New", Courier, monospace;')

                ui.button('📜 Alle Benutzer anzeigen', on_click=show_all_users_dialog).classes(
                    'bg-gradient-to-r from-purple-600 to-pink-500 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                ).style('font-family: "Courier New", Courier, monospace;')

                ui.button('🎒 Benutzer-Items anzeigen', on_click=show_user_items_dialog).classes(
                    'bg-gradient-to-r from-orange-400 to-red-500 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                ).style('font-family: "Courier New", Courier, monospace;')

                ui.button('✨ Neuen Benutzer erstellen',
                          on_click=lambda: ui.run_javascript('window.location.href="/create_user"')).classes(
                    'bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                ).style('font-family: "Courier New", Courier, monospace;')

                ui.button('🔄 Benutzer wechseln', on_click=show_switch_user_dialog).classes(
                    'bg-gradient-to-r from-gray-400 to-gray-600 text-white font-bold text-lg w-full rounded-lg py-3 hover:shadow-xl'
                ).style('font-family: "Courier New", Courier, monospace;')

            # Verfügbare Avatare basierend auf der Rasse anzeigen
            with ui.row().classes('justify-center flex-wrap gap-6 mt-8'):
                for avatar in avatars:
                    with ui.column().classes('items-center gap-2'):
                        ui.image(f'/images/{avatar["path"]}').classes(
                            'w-24 h-24 object-cover rounded-full border border-gray-300 shadow-lg hover:scale-110 transition-transform'
                        )
                        ui.label(avatar["name"]).classes('text-sm font-bold text-gray-700').style(
                            'font-family: "Courier New", Courier, monospace;')

                        ui.button('Auswählen', on_click=lambda a_id=avatar["id"]: change_user_avatar(a_id)).classes(
                            'bg-blue-500 text-white text-xs rounded-md px-4 py-2 hover:bg-blue-600'
                        ).style('font-family: "Courier New", Courier, monospace;')

            # Button für das Hauptmenü
            ui.button('🏠 Zurück zum Hauptmenü',
                      on_click=lambda: ui.run_javascript("window.location.href='/homepage';")).classes(
                'bg-gray-600 text-white font-bold text-lg w-full rounded-lg py-3 mt-6 hover:shadow-xl'
            ).style('font-family: "Courier New", Courier, monospace;')


def change_user_avatar(avatar_id):
    """Ändert den Avatar des aktuellen Benutzers und lädt die Seite neu, um Änderungen anzuzeigen."""
    global user_id
    update_user_avatar(user_id, avatar_id)

    avatar_path = get_avatar_path_by_id(avatar_id)
    if avatar_path:
        with ui.dialog() as dialog:
            with ui.card():
                ui.label('✅ Avatar geändert!').classes('text-2xl font-bold text-center mb-4')
                ui.image(avatar_path).classes('w-32 h-32 rounded-full mx-auto shadow-lg mb-4')
                ui.label('Dein neuer Avatar wurde erfolgreich übernommen!').classes('text-lg text-gray-700 text-center')
                ui.button('Schließen', on_click=lambda: reload_page(dialog)).classes(
                    'mt-4 bg-blue-500 text-white rounded-lg'
                )
            dialog.open()
    else:
        ui.notify('Fehler beim Ändern des Avatars. Bitte versuche es erneut.', color='negative')

def reload_page(dialog):
    """Schließt den Dialog und lädt die Seite neu."""
    dialog.close()
    ui.run_javascript("location.reload()")

def show_user_status_dialog():
    """Zeigt die Details des aktuellen Benutzers in einem Dialogfenster."""
    global user_id
    user = get_user_by_id(user_id)

    if user:
        username, rasse, klasse, avatar_id, level, xp = user
        avatar_path = get_avatar_path_by_id(avatar_id)

        with ui.dialog() as dialog:
            with ui.card():
                ui.label(f'🔍 Benutzerstatus: {username}').classes('text-2xl font-bold text-center mb-4')
                if avatar_path:
                    ui.image(avatar_path).classes('w-32 h-32 rounded-full mx-auto shadow-lg')
                ui.label(f'🏹 Rasse: {rasse}').classes('text-lg text-gray-700')
                ui.label(f'⚔️ Klasse: {klasse}').classes('text-lg text-gray-700')
                ui.label(f'⭐ Level: {level}').classes('text-lg text-gray-700')
                ui.label(f'💎 XP: {xp}').classes('text-lg text-gray-700')
                ui.button('Schließen', on_click=dialog.close).classes('mt-4 bg-blue-500 text-white rounded-lg')
            dialog.open()

def show_all_users_dialog():
    """Zeigt alle Benutzer in einem optimierten Dialogfenster."""
    users = get_all_users()

    with ui.dialog() as dialog:
        # Dialog mit leicht transparenter Hintergrundfarbe
        with ui.card().style('width: 100%; max-width: 900px; background-color: rgba(255, 255, 255, 0.95);'):
            ui.label('📜 Alle Benutzer').classes('text-2xl font-bold text-center mb-4')

            if users:
                # Kopfzeile der Tabelle
                with ui.row().classes('font-bold text-left bg-gray-100 py-1 px-2 rounded-t-lg w-full'):
                    ui.label('Avatar').style('width: 10%; text-align: center;')
                    ui.label('Name').style('width: 20%; text-align: left;')
                    ui.label('Rasse').style('width: 25%; text-align: left;')
                    ui.label('Klasse').style('width: 20%; text-align: left;')
                    ui.label('Level / XP').style('width: 15%; text-align: center;')

                # Benutzerinformationen anzeigen
                for user in users:
                    user_id_in_db, username, rasse, klasse, avatar_id, level, xp = user
                    avatar_path = get_avatar_path_by_id(avatar_id)

                    # Benutzerzeile
                    with ui.row().classes('py-1 px-2 border-b border-gray-200 w-full items-center'):
                        # Avatar
                        with ui.element('div').style(
                            'width: 40px; height: 40px; border-radius: 50%; overflow: hidden; '
                            'display: flex; justify-content: center; align-items: center; background-color: #f0f0f0;'
                        ):
                            ui.image(avatar_path).style('width: 100%; height: 100%; object-fit: cover;')

                        # Name
                        ui.label(username).style('width: 20%; text-align: left;')

                        # Rasse
                        ui.label(rasse).style('width: 25%; text-align: left;')

                        # Klasse
                        ui.label(klasse).style('width: 20%; text-align: left;')

                        # Level / XP kombiniert
                        ui.label(f'Level: {level} | XP: {xp}').style('width: 15%; text-align: center;')
            else:
                ui.label('Keine Benutzer gefunden.').classes('text-center text-gray-500')

            # Schließen-Button in Grau
            ui.button('Schließen', on_click=dialog.close).classes(
                'mt-4 bg-blue-500 text-white rounded-md w-full hover:bg-blue-600'
            )

        dialog.open()


def show_user_items_dialog():
    """Zeigt die Items des aktuellen Benutzers in einem Dialogfenster."""
    global user_id
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
                with ui.row().classes('justify-center flex-wrap gap-6'):
                    for name, path in items:
                        full_path = f'/images/{path}'
                        with ui.column().classes('items-center gap-2'):
                            ui.image(full_path).classes(
                                'w-24 h-24 object-contain rounded-full border border-gray-300 shadow-sm'
                            )
                            ui.label(name).classes('text-center font-bold text-gray-700 text-sm')
            else:
                ui.label('Du hast noch keine Items gesammelt.').classes('text-gray-500 text-center')

            ui.button('Schließen', on_click=dialog.close).classes('mt-4 bg-blue-500 text-white rounded-lg')
        dialog.open()

def show_switch_user_dialog():
    """Zeigt einen Dialog an, um den Benutzer zu wechseln."""
    users = get_all_users()

    with ui.dialog() as dialog:
        with ui.card():
            ui.label('🔄 Benutzer wechseln').classes('text-2xl font-bold text-center mb-4')

            if users:
                with ui.column().classes('gap-4'):
                    for user in users:
                        # Entpacken der Werte basierend auf der erwarteten Struktur
                        user_id_in_db, username, rasse, klasse, avatar_id, level, xp = user[:7]  # Nur die ersten 7 Werte verwenden
                        avatar_path = get_avatar_path_by_id(avatar_id)

                        with ui.row().classes('items-center gap-4'):
                            if avatar_path:
                                ui.image(avatar_path).classes('w-12 h-12 rounded-full shadow-lg')
                            ui.label(username).classes('text-lg font-bold text-gray-700')
                            ui.button('Wechseln', on_click=lambda uid=user_id_in_db: handle_user_switch(uid, dialog)).classes(
                                'bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600'
                            )
            else:
                ui.label('Keine Benutzer vorhanden.').classes('text-lg text-gray-500 text-center')

            ui.button('Schließen', on_click=dialog.close).classes('mt-4 bg-gray-500 text-white rounded-lg')
        dialog.open()

def handle_user_switch(selected_user_id, dialog):
    """Wechselt den Benutzer, schließt den Dialog und lädt die Seite neu."""
    global user_id
    user_id = selected_user_id  # Benutzer-ID aktualisieren
    dialog.close()

    # Hinweis über den Benutzerwechsel anzeigen
    ui.notify(f"Benutzer erfolgreich gewechselt! Neue Benutzer-ID: {user_id}", color='positive')

    # Seite neu laden, um die Änderungen anzuzeigen
    ui.run_javascript("location.reload()")
