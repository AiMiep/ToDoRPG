import sqlite3

# User Klasse
class User:
    def __init__(self, name: str, age: int, gender: str):
        # Überprüfen ob das Geschlecht korrekt ist
        if gender not in ['Männlich', 'Weiblich', 'Divers']:
            raise ValueError("Geschlecht muss 'Männlich', 'Weiblich' oder 'Divers' sein")

        self.name = name
        self.age = age
        self.gender = gender

    def create_user(self):
        connection = connect_database()
        cursor = connection.cursor()

        # User in die Datenbank einfügen
        cursor.execute('''
        INSERT INTO users (name, age, gender) VALUES (?, ?, ?)
        ''', (self.name, self.age, self.gender))

        connection.commit()
        connection.close()
        print(f"User {self.name} erfolgreich angelegt.")

    # Methode zum Löschen eines Nutzers aus der Datenbank
    def delete_user(self, user_id: int):
        connection = connect_database()
        cursor = connection.cursor()

        # User aus der Datenbank löschen
        cursor.execute('''
        DELETE FROM users WHERE id = ?
        ''', (user_id,))

        connection.commit()
        connection.close()
        print(f"User mit ID {user_id} erfolgreich gelöscht.")

# Verbindung zur Datenbank herstellen
def connect_database():
    database = sqlite3.connect('taskify.db')
    return database


# Beispiel für die Verwendung
if __name__ == "__main__":
    # Erstellen eines User-Objekts
    user = User(name="Max Mustermann", age=30, gender="Männlich")

    # User anlegen
    user.create_user()

    # User löschen (Beispiel: User mit ID 1 löschen)
    user.delete_user(1)
