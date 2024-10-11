import os
import time
import csv
import RPi.GPIO as GPIO
import sys
import sqlite3

DATENBANK = 'dbFinal.db'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 17
LED_PIN2 = 27
LED_PIN3 = 12
BUZZER_PIN = 21
TRIG = 23
ECHO = 24
sleeptime = 1

print("\033[94mDie Messung wurde gestartet!\033[0m")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.setup(LED_PIN3, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(TRIG, False)

time.sleep(2)

if len(sys.argv) > 1:
    userID = int(sys.argv[1])
else:
    userID = 0

user_id = userID

def buzzer_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def buzzer_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def distanzMessen():

    for yeah in range(6):
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            messStart = time.time()

        while GPIO.input(ECHO) == 1:
            messEnde = time.time()

        gemesseneZeit = messEnde - messStart
        distanz = gemesseneZeit * 17150
        distanz = round(distanz, 2)

        if (distanz < 10):
            print("\033[91mDie gemessene Distanz beträgt\033[0m", distanz, "cm!")
            GPIO.output(LED_PIN, GPIO.HIGH)
            buzzer_on()
            time.sleep(sleeptime)
            GPIO.output(LED_PIN, GPIO.LOW)
            buzzer_off()

        elif (distanz < 25):
            print("\033[93mDie gemessene Distanz beträgt\033[0m", distanz, "cm!")
            GPIO.output(LED_PIN2, GPIO.HIGH)
            time.sleep(sleeptime)
            GPIO.output(LED_PIN2, GPIO.LOW)

        else:
            print("\033[92mDer Distanz ist ausreichend\033[0m", distanz, "cm!")
            GPIO.output(LED_PIN3, GPIO.HIGH)
            time.sleep(sleeptime)
            GPIO.output(LED_PIN3, GPIO.LOW)
        time.sleep(sleeptime)

        return distanz


def erzeuge_verzeichnisstruktur():

    jahr = time.strftime('%Y')
    monat = time.strftime('%m')
    woche = time.strftime('%W')
    pfad = f"/home/user/Desktop/Distanzmessungen/{jahr}/{monat}/Woche_{woche}"
    os.makedirs(pfad, exist_ok=True)

    return pfad


def messungen_durchfuehren(repeat):

    #pfad = erzeuge_verzeichnisstruktur()
    #dateiname = time.strftime('distanzmessungen_%Y-%m-%d_%H-%M-%S.txt')
    #dateipfad = os.path.join(pfad, dateiname)
    #with open(dateipfad, "w") as file:

    while repeat:
        distanz = distanzMessen()

        if (distanz < 4):
            break;

        #print(f"Gemessene Distanz: {distanz:.1f} cm")
        zeitstempel = time.strftime('%d.%m.%y, %H:%M')
        insert_measurement(user_id, zeitstempel, distanz)
        #file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Gemessene Distanz: {distanz:.1f} cm\n")
        time.sleep(1)


def messungen_durchfuehren2():

    pfad = erzeuge_verzeichnisstruktur()
    dateiname = time.strftime('distanzmessungen_%Y-%m-%d_%H-%M-%S.csv')
    dateipfad = os.path.join(pfad, dateiname)

    with open(dateipfad, "w", newline='') as file:
        csv_writer = csv.writer(file, delimiter=';')
        csv_writer.writerow(["Zeitstempel", "Distanz (cm)"])

        for _ in range(5):
            distanz = distanzMessen()
            zeitstempel = time.strftime('%Y-%m-%d %H:%M:%S')
            #print(f"Gemessene Distanz: {distanz:.1f} cm")
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
    distanzMessen()
    messungen_durchfuehren(True)


#if __name__ == "__main__":
    #messungen_durchfuehren2()
    #messungen_durchfuehren()
