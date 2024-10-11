import tkinter as tk
import sqlite3
import os
import login_gui
import sys
from SammelDaten import runMessung

if len(sys.argv) > 1:
    userID = int(sys.argv[1])
else:
    userID = 0

user_id = userID
start_index = 0


def show_user_data(user_id):
    global start_index
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, login_gui.DATENBANK)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT measurement_data, timestamp FROM messdaten WHERE user_id=? ORDER BY timestamp DESC LIMIT 5 OFFSET ?",
        (user_id, start_index))
    measurements = cursor.fetchall()
    print("Abruf der Messdaten:", measurements)

    if measurements:
        data_str = "\n".join([f"Messung: {m[0]} cm, Uhrzeit: {m[1]} " for m in measurements])
        print("datastring", measurements)
        data_display.config(text=data_str)

    else:
        data_display.config(text="Keine Messdaten verfügbar.")


def next_page(user_id):
    global start_index
    start_index += 5  # Zeige die nächsten 5 Einträge
    show_user_data(user_id)


def prev_page(user_id):
    global start_index
    start_index = max(0, start_index - 5)  # Zeige die vorherigen 5 Einträge, aber nicht unter 0
    show_user_data(user_id)


def del_old_measurements(user_id):
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, login_gui.DATENBANK)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM messdaten WHERE user_id=?
    ''', (user_id,))

    conn.commit()
    conn.close()


root1 = tk.Tk()
root1.geometry("500x500")
root1.title("Deine Daten: ")

data_display = tk.Label(root1, text="Zum Anzeigen ihrer Daten klicken sie auf Voherige Seite", justify='left',
                        anchor='w')
data_display.pack(pady=10)

button_messung = tk.Button(root1, text="Messung starten", command=lambda: runMessung())
button_messung.pack(pady=10)

button_messung = tk.Button(root1, text="Messdaten löschen", command=lambda: del_old_measurements(user_id))
button_messung.pack(pady=10)

button_prev = tk.Button(root1, text="Vorherige Seite", command=lambda: prev_page(user_id))
button_prev.pack(pady=10)

button_next = tk.Button(root1, text="Nächste Seite", command=lambda: next_page(user_id))
button_next.pack(pady=10)

root1.mainloop()
