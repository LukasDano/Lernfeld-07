import sqlite3
import os
 
def setup_database():
    # Verbindung zur Datenbank herstellen
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, 'testdb.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
 
    # Tabelle für Benutzer erstellen
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        user_data TEXT
    )
    ''')
 
    conn.commit()
    conn.close()
 
# Aufruf der Funktion zum Einrichten der Datenbank
setup_database()