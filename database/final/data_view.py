import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import login_gui
import config

start_index = 0
user_id = config.user_id

def show_user_data(user_id):
    global start_index
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, login_gui.DATENBANK)
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()
 
    cursor.execute("SELECT measurement_data, timestamp FROM messdaten WHERE user_id=? ORDER BY timestamp DESC LIMIT 5 OFFSET ?", (user_id, start_index))
    measurements = cursor.fetchall()
    print("Abruf der Messdaten:", measurements)
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

root = tk.Tk()
root.geometry("500x500")
root.title("Deine Daten: ")

data_display = tk.Label(root, text="", justify='left', anchor='w')
data_display.pack(pady=10)

button_prev = tk.Button(root, text="Vorherige Seite", command=lambda: prev_page(user_id))
button_prev.pack(pady=10)
 
button_next = tk.Button(root, text="Nächste Seite", command=lambda: next_page(user_id))
button_next.pack(pady=10)

root.mainloop()
