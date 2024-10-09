import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import subprocess
# import config

DATENBANK= 'dbFinal.db'
start_index = 0
user_id = ""

def login():
    username = entry_username.get()
    password = entry_password.get()
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, DATENBANK)
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        global user_id
        user_id = user[0]
        show_user_data(user_id)
    else:
        messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort")

    conn.close()

def show_user_data(user_id):
    global start_index
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, DATENBANK)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT measurement_data, timestamp FROM messdaten WHERE user_id=? ORDER BY timestamp DESC LIMIT 5 OFFSET ?", (user_id, start_index))
    measurements = cursor.fetchall()
    print("Abruf der Messdaten:", measurements )
    if measurements:
        data_str = "\n".join([f"Messung: {m[1]} cm" for m in measurements])
        print("datastring", data_str)
        data_display.config(text=data_str)
    else:
        data_display.config(text="Keine Messdaten verfügbar.")

def next_page(user_id):
    global start_index
    start_index += 5 # Zeige die nächsten 5 Einträge
    show_user_data(user_id)

def prev_page(user_id):
    global start_index
    start_index = max(0, start_index - 5) # Zeige die vorherigen 5 Einträge, aber nicht unter 0
    show_user_data(user_id)

# Funktion zum Schließen der Anwendung
def close_app():
    root.destroy()

# Funktion, um die Registrierungs-GUI zu öffnen
def open_registration():
    root.destroy() # Schließt die Login-GUI
    subprocess.run(["python3", "register_user.py"]) # Öffnet die Registrierungsseite

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
data_display = tk.Label(root, text="", justify='left', anchor='w')
data_display.pack(pady=10)

# Login-Button
button_login = tk.Button(root, text="Anmelden", command=login)
button_login.pack(pady=20)

# Button zur Registrierung (wenn der Benutzer noch kein Konto hat)
button_register = tk.Button(root, text="Noch keinen Account? Jetzt registrieren!", command=open_registration)
button_register.pack(pady=5)

# Ergebnis-Label für die Benutzerinformationen
#label_result = tk.Label(root, text="", wraplength=300)
#label_result.pack(pady=10)
button_prev = tk.Button(root, text="Vorherige Seite", command=lambda: prev_page(user_id))
button_prev.pack(pady=5)

button_next = tk.Button(root, text="Nächste Seite", command=lambda: next_page(user_id))
button_next.pack(pady=5)

# Schließen-Button
button_close = tk.Button(root, text="Schließen", command=close_app)
button_close.pack(pady=5)

# GUI starten
root.mainloop()