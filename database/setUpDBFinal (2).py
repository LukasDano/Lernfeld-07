import sqlite3
import os

DATENBANK = 'dbFinal.db'
 
def setup_database():
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, DATENBANK)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messdaten (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        timestamp TEXT,
        measurement_data TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    conn.commit()
    conn.close()
 
def insert_measurement(user_id, timestamp, measurement_data):
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, DATENBANK)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
 
    # Messdaten in die Tabelle 'messdaten' einfügen
    cursor.execute('''
    INSERT INTO messdaten (user_id, timestamp, measurement_data)
    VALUES (?, ?, ?)
    ''', (user_id, timestamp, measurement_data))

    conn.commit()
    conn.close()
 
def get_user_measurements(user_id):
  
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, DATENBANK)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
 
 
    cursor.execute('''
    SELECT measurement_data FROM messdaten WHERE user_id=?
    ''', (user_id,))
    measurements = cursor.fetchall()
 
    # Verbindung schließen
    conn.close()
 
    return measurements
 
# Beispiel für die Initialisierung der Datenbank
setup_database()
 

#insert_measurement(1, "1.1.1991", "gemessene Distanz")
 

#user_measurements = get_user_measurements(1)
#print(f"Messdaten für Benutzer 1: {user_measurements}")
 
