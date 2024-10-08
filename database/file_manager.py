import sqlite3
import os
from datetime import datetime, timedelta

HOME_DIR = os.path.expanduser("~")
DB_PATH = os.path.join(HOME_DIR, 'testdb.db')

def add_txt_files_to_db(directory, username):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
 
        # Alle .txt-Dateien im angegebenen Verzeichnis durchlaufen
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
 
                # Hier wird der Dateiname aufgeteilt
                parts = filename.split('_')
                
                # Überprüfen, ob wir genügend Teile haben, um das Datum zu extrahieren
                if len(parts) >= 2:
                    date_part = parts[1]  # Der zweite Teil ist das Datum (z.B. "2024-10-07")
                    
                    try:
                        # Datumsüberprüfung
                        file_date = datetime.strptime(date_part, "%Y-%m-%d").date()
 
                        # Inhalt der Datei lesen
                        with open(file_path, 'r') as file:
                            file_data = file.read()
 
                        # Daten in die Datenbank einfügen
                        cursor.execute('''
                        INSERT INTO users (username, password, user_data)
                        VALUES (?, ?, ?)
                        ''', (username, "dummy_password", file_data))
 
                    except ValueError:
                        print(f"Ungültiges Datum im Dateinamen: {filename}")
                else:
                    print(f"Dateiname hat nicht das erwartete Format: {filename}")
 
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Fehler beim Hinzufügen der Dateien: {e}")
 
    finally:
        if conn:
            conn.close()

def write_data_in_database(username, data):

    try:

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO users (username, password, user_data)
        VALUES (?, ?, ?)
        ''', (username, "dummy_password", data))

        conn.commit()

    except sqlite3.Error as e:
        print(f"Fehler beim Hinzufügen der Daten in die Datenbank: {e}")

    finally:
        if conn:
            conn.close()
    
 
def delete_old_entries(directory):
    # 7 Tage Grenze berechnen
    seven_days_ago = datetime.now().date() - timedelta(days=7)
 
    # Alle Dateien im angegebenen Verzeichnis durchlaufen
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            # Datum aus dem Dateinamen extrahieren
            date_from_filename = filename.replace('.txt', '')
 
            try:
                # Datumsüberprüfung
                file_date = datetime.strptime(date_from_filename, "%Y-%m-%d").date()
 
                # Wenn das Datum älter als 7 Tage ist, Datei löschen
                if file_date < seven_days_ago:
                    file_path = os.path.join(directory, filename)
                    os.remove(file_path)
                    print(f"Datei {filename} wurde gelöscht, da sie älter als 7 Tage ist.")
 
            except ValueError:
                print(f"Ungültiges Datum im Dateinamen: {filename}")

def get_current_week_folder(base_path):
    # Aktuelles Jahr und Woche ermitteln
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]  # ISO Kalenderwoche
    
    # Basis-Pfad zum Jahr
    year_folder = os.path.join(base_path, str(current_year))
    
    # Basis-Pfad zum Monat (aktuellen Monat ermitteln)
    current_month = datetime.now().month
    month_folder = os.path.join(year_folder, f"{current_month:02d}")  # Zwei Ziffern für den Monat
 
    # Basis-Pfad zur aktuellen Woche
    week_folder = os.path.join(month_folder, f"Woche_{current_week}")
 
    # Überprüfen, ob der Ordner existiert, und den Pfad zurückgeben
    if os.path.exists(week_folder):
        return week_folder
    else:
        print(f"Ordner für Woche {current_week} existiert nicht.")
        return None 
base_path = "../Distanzmessungen"

add_txt_files_to_db(get_current_week_folder(base_path), "user")
#delete_old_entries(get_current_week_folder(base_path))
