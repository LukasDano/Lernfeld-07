import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import subprocess

DATENBANK= 'dbFinal.db'
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
        #config.user_id = user[0] 
        #print(f"user id der Config datei: {config.user_id}")
        root.destroy() 
        subprocess.run(["python3", "data_view.py", str(user_id)]) 

    else:
        messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort")

def dev_login():
    
    username = "user"
    password = "user"
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, DATENBANK)
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()
 
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
 
    if user:
        global user_id
        user_id = user[0]
        #config.user_id = user[0] 
        #print(f"user id der Config datei: {config.user_id}")
        root.destroy() 
        subprocess.run(["python3", "data_view.py", str(user_id)]) 

    else:
        messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort") 

def close_app():
    root.destroy()
 
# Funktion, um die Registrierungs-GUI zu öffnen
def open_registration():
    root.destroy()  # Schließt die Login-GUI
    subprocess.run(["python3", "register_user.py"])  # Öffnet die Registrierungsseite
 
if __name__== "__main__": 

    # GUI-Setup für die Anmeldung
    root = tk.Tk()
    root.geometry("500x500")
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
    
    # Login-Button
    button_login = tk.Button(root, text="DEV", command=dev_login)
    button_login.pack(pady=20)
     
    # Button zur Registrierung (wenn der Benutzer noch kein Konto hat)
    button_register = tk.Button(root, text="Noch keinen Account? Jetzt registrieren!", command=open_registration)
    button_register.pack(pady=5)
     
    # Schließen-Button
    button_close = tk.Button(root, text="Schließen", command=close_app)
    button_close.pack(pady=5)
     
    # GUI starten
    root.mainloop()
