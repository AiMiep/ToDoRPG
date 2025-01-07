from database import create_table
import user
from utils import task_manager

def main():
    create_table()
    user.check_if_user_exists()
    task_manager()

main()
