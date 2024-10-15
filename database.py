import sqlite3

def connectDatabase():
    database = sqlite3.connect('taskify.db')
    return database

def createTables():
    database = connectDatabase()
    database.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            age INT,
            gender TEXT
        )
    ''')

    database.execute('''
             CREATE TABLE tasks (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 description TEXT,
                 status TEXT
                 deadline DATE
             )
         ''')

    database.commit()
    database.close()