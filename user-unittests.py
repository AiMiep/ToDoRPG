import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from user import User, connect_database
"""
class TestUser(unittest.TestCase):

    @patch('user.connect_database') #connect_database methode mocken
    def test_create_user(self, mock_connect_database):
        # Setup: Ein Mock für die Verbindung und den Cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        email = 'test@gmx.de'

        # Die Verbindung gibt den Cursor zurück
        mock_connection.cursor.return_value = mock_cursor
        # connect_database gibt die Mock-Verbindung zurück
        mock_connect_database.return_value = mock_connection

        # Ein Beispiel-User-Objekt erstellen
        user = User(email = email, name="Max Mustermann", age=30, gender="Männlich")

        # Methode aufrufen
        user.create_user()

        # Testen, ob die richtigen SQL-Befehle ausgeführt wurden
        mock_cursor.execute.assert_called_once_with(
            'INSERT INTO users (email, name, age, gender) VALUES (?, ?, ?, ?)',
            (email, "Max Mustermann", 30, "Männlich")
        )
        # Testen, ob commit und close aufgerufen wurden
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('user.connect_database')
    def test_delete_user(self, mock_connect_database):
        # Setup: Ein Mock für die Verbindung und den Cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        email = 'test@gmx.de'
        mock_connection.cursor.return_value = mock_cursor
        mock_connect_database.return_value = mock_connection

        # Ein User-Objekt erstellen, um die delete_user Methode aufzurufen
        user = User(email = email, name="Max Mustermann", age=30, gender="Männlich")



        # Methode aufrufen
        user.delete_user(email)


        mock_cursor.execute.assert_any_call(
            'DELETE FROM users WHERE email = ?', (email,)
        )

        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
"""