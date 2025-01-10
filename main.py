from database import create_table
from user import create_new_user, check_if_user_exists
from utils import task_manager

def main():
    create_table()

    # Benutzer prüfen oder erstellen
    if not check_if_user_exists():
        print("Benutzer erstellen:")
        username = input("Benutzername: ").strip()
        create_new_user(username)

    print("\nStarte Task-Manager...")
    task_manager()

if __name__ == "__main__":
    main()
