import sqlite3
import os

DBNAME = "testdb.db"

def view_user_data():
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, 'testdb.db')
 
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
 
        # Abfrage der Daten aus der Tabelle
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
 
        # Ausgabe der Daten
        for row in rows:
            print(row)
 
    except sqlite3.Error as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
 
    finally:
        if conn:
            conn.close()
 
# Funktion aufrufen
view_user_data()
