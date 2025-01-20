import os
from nicegui import ui, app
from user import create_new_user

# Statische Dateien bereitstellen
app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))

# Hintergrund-GIFs oder Bilder für Rassen
RACE_TO_BACKGROUND_GIF = {
    "Mensch (Mario Bros)": "backgroundGif/M-Background.gif",
    "Goronen/Zoras/Rito/Gerudo (Zelda)": "backgroundGif/Z-Background.gif",
    "Pokémon-Trainer (Pokémon)": "backgroundGif/P-Background.gif"
}

# Klassen für jede Rasse
RACE_TO_CLASSES = {
    "Mensch (Mario Bros)": [
        "🦸 Held (Mario)",
        "🦹 Schurke (Waluigi)",
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

# Avatare für jede Kategorie
def get_avatars_by_race(race):
    avatars = {
        "Mensch (Mario Bros)": [
            {"id": 10, "name": "Mario", "path": "newAvatars/M-Mario.jpg"},
            {"id": 11, "name": "Waluigi", "path": "newAvatars/M-Waluigi.jpg"},
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

# CSS zur Entfernung von Rändern und für einen nahtlosen Hintergrund
ui.add_head_html("""
<style>
    html, body {
        margin: 0;
        padding: 0;
        height: 100%;
        overflow: hidden; /* Verhindert Scrollen */
    }
</style>
""")

@ui.page('/create_user')
def user_creation_page():
    """Zeigt die Seite zur Benutzererstellung mit dynamischen Avataren, Klassen und Hintergrund-GIFs."""
    selected_avatar = {'id': None}

    def select_avatar(avatar_id):
        selected_avatar['id'] = avatar_id
        ui.notify(f'Du hast den Avatar mit ID {avatar_id} ausgewählt!')

    # Haupt-Container mit dynamischem Hintergrund
    with ui.column().classes('min-h-screen w-screen justify-center items-center') as page_container:
        page_container.style('background-image: url("/images/backgroundGif/M-Background.gif");'
                             'background-size: cover; background-position: center;')

        with ui.card().classes('bg-gray-100 bg-opacity-80 shadow-lg border-black border rounded-lg w-11/12 sm:w-3/4 md:w-1/2 lg:w-1/3 p-6 mt-6'):
            ui.label('🌟 Charaktererstellung 🌟').classes('text-2xl sm:text-3xl font-bold text-black text-center mt-4')
            ui.label('Gestalte deinen Helden und wähle deinen Avatar!').classes('text-sm text-gray-700 text-center mb-4')

            with ui.column().classes('w-full items-center gap-3'):
                ui.label('🔤 Dein Heldname').classes('text-lg font-bold text-black text-center')
                username = ui.input(placeholder='z. B. Mario oder Zelda').classes('w-full text-sm')

                # Rassenauswahl mit `on_change` direkt integriert
                ui.label('🧝 Wähle eine Rasse').classes('text-lg font-bold text-black text-center mt-3')
                rasse = ui.radio(
                    [
                        "Mensch (Mario Bros)",
                        "Goronen/Zoras/Rito/Gerudo (Zelda)",
                        "Pokémon-Trainer (Pokémon)"
                    ],
                    value="Mensch (Mario Bros)",
                    on_change=lambda: update_page_elements(rasse.value)
                ).classes('text-sm')

                ui.label('🏹 Wähle eine Klasse').classes('text-lg font-bold text-black text-center mt-3')
                class_container = ui.column().classes('w-full items-center gap-3')  # Container für Klassen
                klasse = ui.radio([])  # Leere Optionen initialisieren

            avatar_container = ui.row().classes('justify-center flex-wrap gap-6 mt-4')

            with ui.column().classes('items-center w-full gap-4 mt-6'):
                progress = ui.linear_progress(0).classes('w-3/4')
                ui.button('🚀 Abenteuer starten!', on_click=lambda: create_user_action(username, rasse, klasse, selected_avatar, progress)).classes(
                    'w-1/3 bg-gradient-to-r from-blue-500 to-purple-600 text-white text-sm font-bold py-3 rounded-lg hover:shadow-lg'
                )

    def update_page_elements(selected_race):
        """Aktualisiert Hintergrund-GIF, Avatare und Klassen basierend auf der gewählten Rasse."""
        nonlocal avatar_container, class_container

        # Aktualisiere den Hintergrund
        background_path = RACE_TO_BACKGROUND_GIF.get(selected_race, "backgroundGif/M-Background.gif")
        page_container.style(f'background-image: url("/images/{background_path}"); background-size: cover;'
                             'background-position: center;')

        # Lade Avatare basierend auf der Rasse
        avatars = get_avatars_by_race(selected_race)
        avatar_container.clear()
        avatar_container = ui.row().classes('justify-center flex-wrap gap-4 mt-4')
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

        # Lade Klassen basierend auf der Rasse
        classes = RACE_TO_CLASSES.get(selected_race, [])
        class_container.clear()
        with class_container:
            klasse.value = classes[0] if classes else None
            klasse.options = classes

    update_page_elements("Mensch (Mario Bros)")

    def create_user_action(username, rasse, klasse, selected_avatar, progress):
        if not username.value or not rasse.value or not klasse.value or not selected_avatar['id']:
            ui.notify('Bitte alle Felder ausfüllen und einen Avatar auswählen!', color='negative')
            return

        create_new_user(username.value, rasse.value, klasse.value, selected_avatar['id'])
        ui.notify(f'Willkommen, {username.value}! Dein Abenteuer beginnt!', color='positive')

        progress.set_value(1)
        ui.timer(1, lambda: ui.run_javascript('window.location.href="/homepage"'))
