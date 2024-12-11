from database import get_database_cursor, commit_and_close

# Neuer User erstellen
def create_new_user(username):
    database, cursor = get_database_cursor()

    cursor.execute('SELECT COUNT(*) FROM users')

    cursor.execute(''' 
        INSERT INTO users (username) 
        VALUES (?)
    ''', (username,))

    commit_and_close(database)
    print(f"Benutzer '{username}' erfolgreich erstellt.")

def check_if_user_exists():
    database, cursor = get_database_cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    result = cursor.fetchone()

    if result[0] == 0:
        username = input("Gebe bitte einen Benutzernamen ein: ")
        create_new_user(username)
    else:
        print("User bereits erstellt.")