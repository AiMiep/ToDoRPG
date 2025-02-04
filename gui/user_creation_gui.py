import os
from nicegui import ui, app
from user import create_new_user

# Statische Dateien bereitstellen
app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))
app.add_static_files('/audios', os.path.join(os.getcwd(), 'audios'))

# Hintergrund-GIFs oder Bilder für Rassen
RACE_TO_BACKGROUND_GIF = {
    "Mensch (Mario Bros)": "backgroundGif/M-Background.gif",
    "Goronen/Zoras/Rito/Gerudo (Zelda)": "backgroundGif/Z-Background.gif",
    "Pokémon-Trainer (Pokémon)": "backgroundGif/P-Background.gif"
}

# Soundtracks für jede Rasse
RACE_TO_SOUNDTRACK = {
    "Mensch (Mario Bros)": "M-Audio.mp3",
    "Goronen/Zoras/Rito/Gerudo (Zelda)": "Z-Audio.mp3",
    "Pokémon-Trainer (Pokémon)": "P-Audio.mp3"
}

# Klassen für jede Rasse
RACE_TO_CLASSES = {
    "Mensch (Mario Bros)": [
        "🦸 Held (Mario)",
        "🦹 Schurke (Wario)",
        "👸 Prinzessin (Peach)"
    ],
    "Goronen/Zoras/Rito/Gerudo (Zelda)": [
        "🗡️ Held (Zelda)",
        "🏹 Bogenschütze (Zelda)",
        "📜 Gelehrter (Magier, Zelda)"
    ],
    "Pokémon-Trainer (Pokémon)": [
        "⚔️ Trainer (Pokémon)",
        "🌲 Ranger (Pokémon)",
        "🥊 Kampfkünstler (Pokémon)"
    ]
}

# Avatare für jede Rasse definieren
def get_avatars_by_race(race):
    """Gibt die Avatare für die angegebene Rasse zurück."""
    avatars = {
        "Mensch (Mario Bros)": [
            {"id": 10, "name": "Mario", "path": "newAvatars/M-Mario.jpg"},
            {"id": 11, "name": "Wario", "path": "newAvatars/M-Wario.jpg"},
            {"id": 12, "name": "Peach", "path": "newAvatars/M-Peach.jpg"}
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
    return avatars.get(race, [])

@ui.page('/create_user')
def user_creation_page():
    """Zeigt die Seite zur Erstellung eines neuen Benutzers."""
    selected_avatar = {'id': None}

    # Audioelement mit Standardwert
    audio_element = ui.audio(src=f'/audios/M-Audio.mp3').props('autoplay loop').style('display: none;')

    def select_avatar(avatar_id):
        """Speichert die ID des ausgewählten Avatars."""
        selected_avatar['id'] = avatar_id
        ui.notify(f'Du hast den Avatar mit ID {avatar_id} ausgewählt!')

    # Hauptseite mit dynamischem Hintergrund
    with ui.column().classes('min-h-screen w-screen justify-center items-center') as page_container:
        page_container.style('background-image: url("/images/backgroundGif/M-Background.gif");'
                             'background-size: cover; background-position: center;')

        # Karte zur Benutzererstellung
        with ui.card().classes('bg-gray-100 bg-opacity-80 shadow-lg border-black border rounded-lg w-11/12 sm:w-3/4 md:w-1/2 lg:w-1/3 p-6 mt-6'):
            ui.label('🌟 Charaktererstellung 🌟').classes(
                'text-2xl sm:text-3xl font-bold text-black text-center mt-4'
            ).style('font-family: "Courier New", Courier, monospace;')

            ui.label('Gestalte deinen Helden und wähle deinen Avatar!').classes(
                'text-sm text-gray-700 text-center mb-4'
            ).style('font-family: "Courier New", Courier, monospace;')

            with ui.column().classes('w-full items-center gap-3'):
                # Eingabe des Benutzernamens
                ui.label('Dein Benutzername').classes(
                    'text-lg font-bold text-black text-center'
                ).style('font-family: "Courier New", Courier, monospace;')

                username = ui.input(placeholder='z. B. Mario oder Zelda').classes('w-full text-sm').style(
                    'font-family: "Courier New", Courier, monospace;')

                # Rassenauswahl
                ui.label('🧝 Wähle eine Rasse').classes(
                    'text-lg font-bold text-black text-center mt-3'
                ).style('font-family: "Courier New", Courier, monospace;')

                rasse = ui.radio(
                    [
                        "Mensch (Mario Bros)",
                        "Goronen/Zoras/Rito/Gerudo (Zelda)",
                        "Pokémon-Trainer (Pokémon)"
                    ],
                    value=None,  # Keine Auswahl zu Beginn
                    on_change=lambda: update_page_elements(rasse.value)
                ).classes('text-sm').style('font-family: "Courier New", Courier, monospace;')

                # Klassen-Auswahl
                ui.label('🏹 Wähle eine Klasse').classes(
                    'text-lg font-bold text-black text-center mt-3'
                ).style('font-family: "Courier New", Courier, monospace;')

                class_container = ui.column().classes('w-full items-center gap-3')
                klasse = ui.radio([]).style('font-family: "Courier New", Courier, monospace;')

            avatar_wrapper = ui.column().classes('w-full items-center mt-4')

            # Fortschrittsanzeige und Button zum Erstellen
            with ui.column().classes('items-center w-full gap-4 mt-6'):
                progress = ui.linear_progress(0).classes('w-3/4')
                ui.button('🚀 Abenteuer starten!', on_click=lambda: create_user_action(username, rasse, klasse, selected_avatar, progress)).classes(
                    'w-1/3 bg-gradient-to-r from-blue-500 to-purple-600 text-white text-sm font-bold py-3 rounded-lg hover:shadow-lg'
                ).style('font-family: "Courier New", Courier, monospace;')

    def update_page_elements(selected_race):
        """Aktualisiert Hintergrund-GIF, Avatare, Klassen und Soundtrack basierend auf der gewählten Rasse."""
        nonlocal avatar_wrapper, class_container

        # Hintergrund aktualisieren
        background_path = RACE_TO_BACKGROUND_GIF.get(selected_race, "backgroundGif/M-Background.gif")
        page_container.style(f'background-image: url("/images/{background_path}"); background-size: cover;'
                             'background-position: center;')

        # Soundtrack aktualisieren
        soundtrack = RACE_TO_SOUNDTRACK.get(selected_race, None)
        if soundtrack:
            audio_element.set_source(f'/audios/{soundtrack}')

        # **Avatar-Wrapper leeren und neuen Avatar-Container hinzufügen**
        avatar_wrapper.clear()

    # **Avatar-Container NEU setzen (mit `ui.row()`)**
        with avatar_wrapper:
            avatar_container = ui.row().classes('justify-center flex-wrap gap-4 mt-2')

            # Avatare basierend auf der Rasse hinzufügen
            avatars = get_avatars_by_race(selected_race) if selected_race else []
            with avatar_container:
                for avatar in avatars:
                    with ui.column().classes('items-center justify-center gap-2') \
                            .style('text-align: center; width: 7rem;'):
                        ui.image(f'/images/{avatar["path"]}').classes(
                            'w-20 h-20 object-cover rounded-full border border-gray-300 shadow-sm'
                        )
                        ui.label(avatar['name']).classes('text-center font-bold text-gray-700 text-sm')
                        ui.button(
                            'AUSWÄHLEN',
                            on_click=lambda a_id=avatar['id']: select_avatar(a_id)
                        ).classes('bg-blue-500 text-white text-xs font-semibold rounded-md py-2 px-4 hover:bg-blue-600')

        # **Klassen-Container leeren**
        class_container.clear()

        # Klassen basierend auf der Rasse laden
        classes = RACE_TO_CLASSES.get(selected_race, [])
        with class_container:
            klasse.options = classes  # Aktualisiere die Optionen der Klasse
            if classes:
                klasse.value = classes[0]  # Standardwert setzen
            else:
                klasse.value = None

    def create_user_action(username, rasse, klasse, selected_avatar, progress):
        """Erstellt einen neuen Benutzer mit den eingegebenen Daten."""
        if not username.value or not rasse.value or not klasse.value or not selected_avatar['id']:
            ui.notify('Bitte alle Felder ausfüllen und einen Avatar auswählen!', color='negative')
            return

        create_new_user(username.value, rasse.value, klasse.value, selected_avatar['id'])
        ui.notify(f'Willkommen, {username.value}! Dein Abenteuer beginnt!', color='positive')

        # Fortschrittsanzeige
        progress.set_value(1)
        ui.timer(1, lambda: ui.run_javascript('window.location.href="/homepage"'))


