import os
import time
import csv
import RPi.GPIO as GPIO
import sys
import sqlite3

DATENBANK = 'dbFinal.db'
SLEEPTIME = 1

LED_PIN = 17
LED_PIN2 = 27
LED_PIN3 = 12
BUZZER_PIN = 21
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.setup(LED_PIN3, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(TRIG, False)

if len(sys.argv) > 1:
    userID = int(sys.argv[1])
else:
    userID = 0

user_id = userID


def buzzer_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)


def buzzer_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)


def distanz_messen():
    for yeah in range(6):
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            mess_start = time.time()

        while GPIO.input(ECHO) == 1:
            mess_ende = time.time()

        gemessene_zeit = mess_ende - mess_start
        distanz = gemessene_zeit * 17150
        distanz = round(distanz, 2)

        if distanz < 10:
            print("\033[91mDie gemessene Distanz beträgt\033[0m", distanz, "cm!")
            GPIO.output(LED_PIN, GPIO.HIGH)
            buzzer_on()
            time.sleep(SLEEPTIME)
            GPIO.output(LED_PIN, GPIO.LOW)
            buzzer_off()

        elif distanz < 25:
            print("\033[93mDie gemessene Distanz beträgt\033[0m", distanz, "cm!")
            GPIO.output(LED_PIN2, GPIO.HIGH)
            time.sleep(SLEEPTIME)
            GPIO.output(LED_PIN2, GPIO.LOW)

        else:
            print("\033[92mDer Distanz ist ausreichend\033[0m", distanz, "cm!")
            GPIO.output(LED_PIN3, GPIO.HIGH)
            time.sleep(SLEEPTIME)
            GPIO.output(LED_PIN3, GPIO.LOW)

        time.sleep(SLEEPTIME)
        return distanz


def erzeuge_verzeichnisstruktur():
    jahr = time.strftime('%Y')
    monat = time.strftime('%m')
    woche = time.strftime('%W')
    pfad = f"/home/user/Desktop/Distanzmessungen/{jahr}/{monat}/Woche_{woche}"
    os.makedirs(pfad, exist_ok=True)

    return pfad


def messungen_durchfuehren():
    while True:
        distanz = distanz_messen()

        if distanz < 4:
            break;

        zeitstempel = time.strftime('%d.%m.%y, %H:%M')
        insert_measurement(user_id, zeitstempel, distanz)
        time.sleep(1)


def messungen_durchfuehren2():
    pfad = erzeuge_verzeichnisstruktur()
    dateiname = time.strftime('distanzmessungen_%Y-%m-%d_%H-%M-%S.csv')
    dateipfad = os.path.join(pfad, dateiname)

    with open(dateipfad, "w", newline='') as file:
        csv_writer = csv.writer(file, delimiter=';')
        csv_writer.writerow(["Zeitstempel", "Distanz (cm)"])

        for _ in range(5):
            distanz = distanz_messen()
            zeitstempel = time.strftime('%Y-%m-%d %H:%M:%S')
            csv_writer.writerow([zeitstempel, f"{distanz:.1f}"])
            time.sleep(1)


def insert_measurement(user_id, timestamp, measurement_data):
    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, DATENBANK)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO messdaten (user_id, timestamp, measurement_data)
    VALUES (?, ?, ?)
    ''', (user_id, timestamp, measurement_data))

    conn.commit()
    conn.close()


def runMessung():
    distanz_messen()
    messungen_durchfuehren()
