import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

def login():

    username = entry_username.get()
    password = entry_password.get()

    # Verbindung zur Datenbank herstellen
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, 'user_data.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Benutzer in der Datenbank suchen
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login erfolgreich", f"Willkommen, {username}!\nDeine Daten: {user[3]}")
    else:
        messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort")

    conn.close()


# Funktion zum Schließen der Anwendung
def close_app():
    root.destroy()


# GUI-Setup
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

# Schließen-Button
button_close = tk.Button(root, text="Schließen", command=close_app)
button_close.pack(pady=5)

# GUI starten
root.mainloop()
