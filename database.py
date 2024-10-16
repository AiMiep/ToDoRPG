import sqlite3


def connectDatabase():
    database = sqlite3.connect('taskify.db')
    return database


def createTables():
    database = connectDatabase()

    # Create 'users' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            age INT,
            gender TEXT
        )
    ''')

    # Create 'tasks' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            status TEXT,
            deadline DATE
        )
    ''')

    database.commit()
    database.close()
