from database import create_table
from user import initialize_user
from utils import task_manager

def main():
    create_table()

    # Benutzer initialisieren
    initialize_user()

    print("\nStarte Task-Manager...")
    task_manager()

if __name__ == "__main__":
    main()
