import os
from nicegui import ui, app
from user import create_new_user

# Statische Dateien bereitstellen
app.add_static_files('/images', os.path.join(os.getcwd(), 'images'))

# Hintergrund-GIFs oder Bilder für Rassen
RACE_TO_BACKGROUND_GIF = {
    "Menschen (Pokémon & Animal Crossing)": "backgroundGif/AC-P-BackgroundGif.gif",
    "Goronen/Zoras/Rito/Gerudo (Zelda)": "backgroundGif/Z-BackgroundGif.gif",
    "Dorfbewohner (Animal Crossing)": "backgroundGif/AC-BackgroundGif.gif",
    "Pokémon-Trainer (Pokémon)": "backgroundGif/P-BackgroundGif.gif"
}

# Klassen für jede Rasse
RACE_TO_CLASSES = {
    "Menschen (Pokémon & Animal Crossing)": [
        "🛍️ Händler (Animal Crossing)",
        "🏗️ Baumeister (Animal Crossing)",
        "🌿 Gärtner (Animal Crossing)",
        "⚔️ Trainer (Pokémon)",
        "🌲 Ranger (Pokémon)",
        "🥊 Kampfkünstler (Pokémon)"
    ],
    "Goronen/Zoras/Rito/Gerudo (Zelda)": [
        "🗡️ Held (Zelda)",
        "🏹 Bogenschütze (Zelda)",
        "📜 Gelehrter (Magier, Zelda)"
    ],
    "Dorfbewohner (Animal Crossing)": [
        "🛍️ Händler (Animal Crossing)",
        "🏗️ Baumeister (Animal Crossing)",
        "🌿 Gärtner (Animal Crossing)"
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
        "Animal Crossing": [
            {"id": 1, "name": "Händler", "path": "newAvatars/AC-Haendler.png"},
            {"id": 2, "name": "Baumeister", "path": "newAvatars/AC-Baumeister.png"},
            {"id": 3, "name": "Gärtner", "path": "newAvatars/AC-Gaertner.png"}
        ],
        "Pokémon": [
            {"id": 4, "name": "Trainer", "path": "newAvatars/P-Trainer.jpg"},
            {"id": 5, "name": "Ranger", "path": "newAvatars/P-Ranger.jpg"},
            {"id": 6, "name": "Kampfkünstler", "path": "newAvatars/P-Brawler.jpg"}
        ],
        "Zelda": [
            {"id": 7, "name": "Held", "path": "newAvatars/Z-Held.jpg"},
            {"id": 8, "name": "Bogenschütze", "path": "newAvatars/Z-Bogen.jpg"},
            {"id": 9, "name": "Gelehrter", "path": "newAvatars/Z-Gelehrter.jpg"}
        ],
        "Default": [
            {"id": 1, "name": "Standard", "path": "newAvatars/Default.png"}
        ]
    }
    return avatars.get(race, avatars["Default"])

@ui.page('/create_user')
def user_creation_page():
    """Zeigt die Seite zur Benutzererstellung mit dynamischen Avataren, Klassen und Hintergrund-GIFs."""
    selected_avatar = {'id': None}

    def select_avatar(avatar_id):
        selected_avatar['id'] = avatar_id
        ui.notify(f'Du hast den Avatar mit ID {avatar_id} ausgewählt!')

    # Haupt-Container mit dynamischem Hintergrund
    with ui.column().classes('min-h-screen w-screen justify-start items-center') as page_container:
        page_container.style('background-image: url("backgroundGif/DefaultBackgroundGif.gif"); background-size: cover; background-position: center;')

        with ui.card().classes('bg-gray-100 bg-opacity-80 shadow-lg border-black border rounded-lg w-11/12 sm:w-3/4 md:w-2/3 p-8 mt-6'):
            ui.label('🌟 Charaktererstellung 🌟').classes('text-2xl sm:text-3xl font-bold text-black text-center mt-4')
            ui.label('Gestalte deinen Helden und wähle deinen Avatar!').classes('text-sm text-gray-700 text-center mb-6')

            with ui.column().classes('w-full items-center gap-4'):
                ui.label('🔤 Dein Heldname').classes('text-lg font-bold text-black text-center')
                username = ui.input(placeholder='z. B. Ash oder Zelda').classes('w-full text-sm')

                # Rassenauswahl mit `on_change` direkt integriert
                ui.label('🧝 Wähle eine Rasse').classes('text-lg font-bold text-black text-center mt-4')
                rasse = ui.radio(
                    [
                        "Menschen (Pokémon & Animal Crossing)",
                        "Goronen/Zoras/Rito/Gerudo (Zelda)",
                        "Dorfbewohner (Animal Crossing)",
                        "Pokémon-Trainer (Pokémon)"
                    ],
                    value="Menschen (Pokémon & Animal Crossing)",
                    on_change=lambda: update_page_elements(rasse.value)
                ).classes('text-sm')

                ui.label('🏹 Wähle eine Klasse').classes('text-lg font-bold text-black text-center mt-4')
                class_container = ui.column().classes('w-full items-center gap-4')  # Container für Klassen
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
        background_path = RACE_TO_BACKGROUND_GIF.get(selected_race, "backgroundGif/DefaultBackgroundGif.gif")
        page_container.style(f'background-image: url("/images/{background_path}"); background-size: cover; background-position: center;')

        # Lade Avatare basierend auf der Rasse
        race_to_category = {
            "Menschen (Pokémon & Animal Crossing)": "Animal Crossing",
            "Goronen/Zoras/Rito/Gerudo (Zelda)": "Zelda",
            "Dorfbewohner (Animal Crossing)": "Animal Crossing",
            "Pokémon-Trainer (Pokémon)": "Pokémon"
        }
        selected_race_category = race_to_category.get(selected_race, "Default")
        avatars = get_avatars_by_race(selected_race_category)

        avatar_container.clear()
        # Avatare-Container
        avatar_container = ui.row().classes('justify-center flex-wrap gap-6 mt-4')
        with avatar_container:
            for avatar in avatars:
                # Vertikale Ausrichtung für Avatar-Bild, Text und Button
                with ui.column().classes('items-center justify-center gap-2') \
                        .style('text-align: center; width: 8rem;'):
                    ui.image(f'/images/{avatar["path"]}').classes(
                        'w-24 h-24 object-cover rounded-full border border-gray-300 shadow-sm'
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

    update_page_elements("Menschen (Pokémon & Animal Crossing)")

    def create_user_action(username, rasse, klasse, selected_avatar, progress):
        if not username.value or not rasse.value or not klasse.value or not selected_avatar['id']:
            ui.notify('Bitte alle Felder ausfüllen und einen Avatar auswählen!', color='negative')
            return

        create_new_user(username.value, rasse.value, klasse.value, selected_avatar['id'])
        ui.notify(f'Willkommen, {username.value}! Dein Abenteuer beginnt!', color='positive')

        progress.set_value(1)
        ui.timer(1, lambda: ui.run_javascript('window.location.href="/homepage"'))
