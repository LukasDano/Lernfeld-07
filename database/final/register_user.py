import sqlite3
import os
import tkinter as tk
from tkinter import messagebox
import subprocess

DATENBANK= 'dbFinal.db' 
def register_user():
    username = entry_username.get()
    password = entry_password.get()
 
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, DATENBANK)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
        ''', (username, password)) 
 
        conn.commit()
        messagebox.showinfo("Registrierung erfolgreich", "Benutzer erfolgreich registriert!")
 
       
        open_login()
 
    except sqlite3.Error as e:
        messagebox.showerror("Fehler", f"Fehler bei der Registrierung: {e}")
 
    finally:
        if conn:
            conn.close()
def open_login():
    root.destroy()
    subprocess.run(["python3", "login_gui.py"])  
 

root = tk.Tk()
root.title("Benutzerregistrierung")

label_username = tk.Label(root, text="Benutzername")
label_username.pack(pady=5)
 
entry_username = tk.Entry(root)
entry_username.pack(pady=5)
 

label_password = tk.Label(root, text="Passwort")
label_password.pack(pady=5)
 
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)
 

button_register = tk.Button(root, text="Registrieren", command=register_user)
button_register.pack(pady=20)
 

button_login = tk.Button(root, text="Zurück zum Login", command=open_login)
button_login.pack(pady=5)

root.mainloop()
