import sqlite3
import os

def register_user(username, password, user_data):

    try:
        # Datenbankverbindung herstellen
        home_dir = os.path.expanduser("~")
        db_path = os.path.join(home_dir, 'user_data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Benutzer zur Datenbank hinzufügen
        cursor.execute('''
        INSERT INTO users (username, password, user_data)
        VALUES (?, ?, ?)
        ''', (username, password, user_data))

        conn.commit()
        print("Benutzer erfolgreich registriert!")

    except sqlite3.Error as e:
        print(f"Fehler bei der Registrierung: {e}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":

    # Beispielaufruf der Funktion
    username = input("Benutzername: ")
    password = input("Passwort: ")
    user_data = input("Zusätzliche Benutzerdaten: ")

    register_user(username, password, user_data)
