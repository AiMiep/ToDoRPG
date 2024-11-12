from database import create_table
from utils import user_manager, task_manager, show_login_options

def main():
    create_table()

    logged_in = False
    user_email = ""

    while not logged_in:
        user_email = show_login_options()
        if user_email:
            logged_in = True
        else:
            print("Anmeldung oder Registrierung fehlgeschlagen. Bitte versuche es erneut.")

    while True:
        print("\nWas möchtest du tun?")
        print("1. User-Management")
        print("2. Task-Management")
        print("3. Beenden")

        choice = input("Wähle eine Option (1-3): ")

        if choice == '1':
            user_manager()
        elif choice == '2':
            task_manager(user_email)
        elif choice == '3':
            print("Programm wird beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")

main()
