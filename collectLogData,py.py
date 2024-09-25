import os
import time
import csv


def erzeuge_verzeichnisstruktur():
    jahr = time.strftime('%Y')
    monat = time.strftime('%m')
    woche = time.strftime('%W')
    pfad = f"C:\\Users\\klaus\\Desktop\\Distanzmessungen\\{jahr}\\{monat}\\Woche_{woche}"
    os.makedirs(pfad, exist_ok=True)
    return pfad


def messungen_durchfuehren():
    pfad = erzeuge_verzeichnisstruktur()
    dateiname = time.strftime('distanzmessungen_%Y-%m-%d_%H-%M-%S.txt')
    dateipfad = os.path.join(pfad, dateiname)
    with open(dateipfad, "w") as file:
        for _ in range(5):
            distanz = 3
            print(f"Gemessene Distanz: {distanz:.1f} cm")
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Gemessene Distanz: {distanz:.1f} cm\n")
            time.sleep(1)


def messungen_durchfuehren2():
    pfad = erzeuge_verzeichnisstruktur()
    dateiname = time.strftime('distanzmessungen_%Y-%m-%d_%H-%M-%S.csv')
    dateipfad = os.path.join(pfad, dateiname)
    with open(dateipfad, "w", newline='') as file:
        csv_writer = csv.writer(file, delimiter=';')
        csv_writer.writerow(["Zeitstempel", "Distanz (cm)"])
        for _ in range(5):
            distanz = 3
            zeitstempel = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"Gemessene Distanz: {distanz:.1f} cm")
            csv_writer.writerow([zeitstempel, f"{distanz:.1f}"])
            time.sleep(1)


messungen_durchfuehren2()
messungen_durchfuehren()
