import sqlite3

# Verbindung zur Datenbank herstellen
def connect_database():
    database = sqlite3.connect('taskify.db')
    return database

# Funktion zum Benutzer hinzufügen
def add_user_to_database(username, age, gender):
    database = connect_database()
    cursor = database.cursor()

    cursor.execute('''
    INSERT INTO users (username, age, gender) VALUES (?, ?, ?)
    ''', (username, age, gender))

    print(f"Füge folgenden Benutzer in die Datenbank ein: {username}, {age}, {gender}")

    database.commit()
    database.close()

# Funktion zum Eingeben eines Usernames
def enter_username():
    username = input("Gebe bitte jetzt einen Benutzernamen ein :) : ")
    return username


# Funktion zum Eingeben des Alters
def enter_age():
    while True:
        try:
            age = int(input("Wie alt bist du ? : "))
            if age > 0:
                return age
            else:
                print("Dein Alter kann nicht im negativen Bereich liegen >:( ")
        except ValueError:
            print("Bitte gebe dein richtiges Alter an - Danke.")


# Funktion zum Auswählen des Geschlechts
def select_gender():
    gender_options = {"1": "Männlich", "2": "Weiblich", "3": "Divers"}
    while True:
        print("Zu welchem Geschlecht gehörst du - wähle aus:")
        for key, value in gender_options.items():
            print(f"{key}: {value}")

        choice = input("Du bist also (1/2/3): ")
        if choice in gender_options:
            return gender_options[choice]
        else:
            print("Ungültige Auswahl. Bitte wählen Sie 1, 2 oder 3.")


# Funktion, um alle Informationen zusammenzuführen
def create_user():
    print("Erstellen Sie einen neuen Benutzer.")
    username = enter_username()
    age = enter_age()
    gender = select_gender()

    add_user_to_database(username, age, gender)

    print("\nBenutzer erstellt - vielen Dank :) :")
    print(f"Benutzername: {username}")
    print(f"Alter: {age}")
    print(f"Geschlecht: {gender}")

create_user()

# Kommentar