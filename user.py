import sqlite3

# User Klasse
class User:
    def __init__(self, name: str, age: int, gender: str, email: str):
        # Überprüfen ob das Geschlecht korrekt ist
        if gender not in ['Männlich', 'Weiblich', 'Divers']:
            raise ValueError("Geschlecht muss 'Männlich', 'Weiblich' oder 'Divers' sein")

        self.name = name
        self.age = age
        self.gender = gender
        self.email = email

    def create_user(self):
        try:
            connection = connect_database()
            cursor = connection.cursor()

            # User in die Datenbank einfügen
            cursor.execute('''INSERT INTO users (email, name, age, gender) VALUES (?, ?, ?, ?)''',
                           (self.email, self.name, self.age, self.gender))

            connection.commit()
            connection.close()
            print(f"User {self.name} erfolgreich angelegt.")
        except sqlite3.Error as e:
            print(f"Fehler beim Anlegen des Users: {e}")



    # Methode zum Löschen eines Nutzers aus der Datenbank
    def delete_user(self, user_email: str):
        connection = connect_database()
        cursor = connection.cursor()

        # Prüfen, ob der User existiert
        cursor.execute('SELECT * FROM users WHERE email = ?', (user_email,))
        user = cursor.fetchone()

        if user is None:
            print(f"Kein User mit Email {user_email} gefunden.")
            return

        # User aus der Datenbank löschen
        cursor.execute('''DELETE FROM users WHERE email = ?''',
                       (user_email,))

        connection.commit()
        connection.close()
        print(f"User mit Email {user_email} erfolgreich gelöscht.")

# Verbindung zur Datenbank herstellen
def connect_database():
    try:
        database = sqlite3.connect('taskify.db')
        return database
    except sqlite3.Error as e:
        print(f"Fehler beim Verbinden mit der Datenbank: {e}")
        return None


# Beispiel für die Verwendung
if __name__ == "__main__":
    # Erstellen eines User-Objekts
    user = User(name="Max Mustermann", age=30, gender="Männlich")

    # User anlegen
    user.create_user()

    # User löschen (Beispiel: User mit email 1 löschen)
    user.delete_user(1)
