import sqlite3
import os

def setup_database():
    # Verbindung zur Datenbank herstellen
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, 'dbFinal.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Erstellen der 'users'-Tabelle ohne 'user_data'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Erstellen der 'messdaten'-Tabelle
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messdaten (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        measurement_data TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Commit und Verbindung schließen
    conn.commit()
    conn.close()

def insert_measurement(user_id, measurement_data):
    # Verbindung zur Datenbank herstellen
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, 'user_data.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Messdaten in die Tabelle 'messdaten' einfügen
    cursor.execute('''
    INSERT INTO messdaten (user_id, measurement_data)
    VALUES (?, ?)
    ''', (user_id, measurement_data))

    # Commit und Verbindung schließen
    conn.commit()
    conn.close()

def get_user_measurements(user_id):
    # Verbindung zur Datenbank herstellen
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, 'user_data.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Messdaten des Benutzers abrufen
    cursor.execute('''
    SELECT measurement_data FROM messdaten WHERE user_id=?
    ''', (user_id,))
    measurements = cursor.fetchall()

    # Verbindung schließen
    conn.close()

    return measurements

# Beispiel für die Initialisierung der Datenbank
setup_database()

# Beispiel für das Einfügen von Messdaten
# Angenommen, user_id ist 1 und Messdaten sind ein Teststring
insert_measurement(1, "Testmessung 2024-10-07")

# Beispiel für das Abrufen von Messdaten für einen Benutzer
user_measurements = get_user_measurements(1)
print(f"Messdaten für Benutzer 1: {user_measurements}")