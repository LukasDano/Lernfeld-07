import sqlite3
import os
import tkinter as tk
from tkinter import messagebox
import subprocess
 
def register_user():
    username = entry_username.get()
    password = entry_password.get()
 
    # Datenbankverbindung herstellen
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, 'testdb.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
 
        # Benutzer zur Datenbank hinzufügen
        cursor.execute('''
        INSERT INTO users (username, password, user_data)
        VALUES (?, ?, ?)
        ''', (username, password, ""))  # user_data initial leer
 
        conn.commit()
        messagebox.showinfo("Registrierung erfolgreich", "Benutzer erfolgreich registriert!")
 
        # Zurück zur Login-Seite nach erfolgreicher Registrierung
        open_login()
 
    except sqlite3.Error as e:
        messagebox.showerror("Fehler", f"Fehler bei der Registrierung: {e}")
 
    finally:
        if conn:
            conn.close()
 
# Funktion, um die Login-GUI zu öffnen
def open_login():
    root.destroy()  # Schließt die Registrierungs-GUI
    subprocess.run(["python3", "login_gui.py"])  # Öffnet die Login-Seite
 
# GUI-Setup für die Registrierung
root = tk.Tk()
root.title("Benutzerregistrierung")
 
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
 
# Registrierungs-Button
button_register = tk.Button(root, text="Registrieren", command=register_user)
button_register.pack(pady=20)
 
# Button zurück zur Login-Seite
button_login = tk.Button(root, text="Zurück zum Login", command=open_login)
button_login.pack(pady=5)
 
# GUI starten
root.mainloop()
