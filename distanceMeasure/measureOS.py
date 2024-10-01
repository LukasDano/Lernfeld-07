import os
import time
import csv
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN_RED = 17
LED_PIN_WHITE = 27
LED_PIN_GREEN = 16
TRIG = 23
ECHO = 24

SLEEP_TIME = 1
REPEATS = 6

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN_RED, GPIO.OUT)
GPIO.setup(LED_PIN_WHITE, GPIO.OUT)
GPIO.setup(LED_PIN_GREEN, GPIO.OUT)
GPIO.output(TRIG, False)
time.sleep(SLEEP_TIME)

print("\033[94mDie Messung wurde gestartet!\033[0m")

def distanzMessen():

  for yeah in range(REPEATS):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        messStart = time.time()

    while GPIO.input(ECHO)==1:
        messEnde = time.time()

    gemesseneZeit = messEnde - messStart
    distanz = gemesseneZeit * 17150
    distanz = round(distanz, 2)
    
    if(distanz < 10):

        print("\033[91mDie gemessene Distanz beträgt\033[0m", distanz, "cm!")
        GPIO.output(LED_PIN_RED, GPIO.HIGH)
        time.sleep(SLEEP_TIME)
        GPIO.output(LED_PIN_RED, GPIO.LOW)

    elif(distanz < 25):

        print("\033[93mDie gemessene Distanz beträgt\033[0m", distanz, "cm!")
        GPIO.output(LED_PIN_WHITE, GPIO.HIGH)
        time.sleep(SLEEP_TIME)
        GPIO.output(LED_PIN_WHITE, GPIO.LOW)

    else:

        print("\033[92mDer Distanz ist ausreichend\033[0m", distanz, "cm!")
        GPIO.output(LED_PIN_GREEN, GPIO.HIGH)
        time.sleep(SLEEP_TIME)
        GPIO.output(LED_PIN_GREEN, GPIO.LOW)

    return distanz

def erzeuge_verzeichnisstruktur():

    jahr = time.strftime('%Y')
    monat = time.strftime('%m')
    woche = time.strftime('%W')
    pfad = f"/home/lukas/Desktop/Distanzmessungen/{jahr}/{monat}/Woche_{woche}"
    os.makedirs(pfad, exist_ok=True)

    return pfad

def messungen_durchfuehren():

    pfad = erzeuge_verzeichnisstruktur()
    dateiname = time.strftime('distanzmessungen_%Y-%m-%d_%H-%M-%S.txt')
    dateipfad = os.path.join(pfad, dateiname)

    with open(dateipfad, "w") as file:

        for _ in range(REPEATS):
          distanz = distanzMessen()
          #print(f"Gemessene Distanz: {distanz:.1f} cm")
          file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Gemessene Distanz: {distanz:.1f} cm\n")
          time.sleep(SLEEP_TIME)

def messungen_durchfuehren2():

    pfad = erzeuge_verzeichnisstruktur()
    dateiname = time.strftime('distanzmessungen_%Y-%m-%d_%H-%M-%S.csv')
    dateipfad = os.path.join(pfad, dateiname)

    with open(dateipfad, "w", newline='') as file:

        csv_writer = csv.writer(file, delimiter=';')
        csv_writer.writerow(["Zeitstempel", "Distanz (cm)"])

        for _ in range(REPEATS):

            distanz = distanzMessen()
            zeitstempel = time.strftime('%Y-%m-%d %H:%M:%S')
            #print(f"Gemessene Distanz: {distanz:.1f} cm")
            csv_writer.writerow([zeitstempel, f"{distanz:.1f}"])
            time.sleep(SLEEP_TIME)


messungen_durchfuehren2()
messungen_durchfuehren()
