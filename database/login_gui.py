import tkinter as tk
import sqlite3
import os
import subprocess

from database import showData
 
def login():
    username = entry_username.get()
    password = entry_password.get()
 
    # Verbindung zur Datenbank herstellen
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(showData.DBNAME)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
 
    # Benutzer in der Datenbank suchen
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
 
    if user:
        # Benutzerinformationen anzeigen
        label_result.config(text=f"Willkommen, {user[1]}!\nDeine Daten: {user[3]}")
    else:
        label_result.config(text="Falscher Benutzername oder Passwort")
 
    conn.close()
 
# Funktion zum Schließen der Anwendung
def close_app():
    root.destroy()
 
# Funktion, um die Registrierungs-GUI zu öffnen
def open_registration():
    root.destroy()  # Schließt die Login-GUI
    subprocess.run(["python3", "register_user.py"])  # Öffnet die Registrierungsseite
 
# GUI-Setup für die Anmeldung
root = tk.Tk()
root.title("Login")
 
# Benutzername
label_username = tk.Label(root, text="Benutzername")
label_username.pack(pady=5)
 
entry_username = tk.Entry(root)
entry_username.pack(pady=5)
 
# Passwort
label_password = tk.Label(root, text="Passwort")
label_password.pack(pady=5)
 
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)
 
# Login-Button
button_login = tk.Button(root, text="Anmelden", command=login)
button_login.pack(pady=20)
 
# Button zur Registrierung (wenn der Benutzer noch kein Konto hat)
button_register = tk.Button(root, text="Noch keinen Account? Jetzt registrieren!", command=open_registration)
button_register.pack(pady=5)
 
# Ergebnis-Label für die Benutzerinformationen
label_result = tk.Label(root, text="", wraplength=300)
label_result.pack(pady=10)
 
# Schließen-Button
button_close = tk.Button(root, text="Schließen", command=close_app)
button_close.pack(pady=5)
 
# GUI starten
root.mainloop()
