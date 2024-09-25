import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 17
LED_PIN2 = 27
TRIG = 23
ECHO = 24

print("\033[94mDie Messung wurde gestartet!\033[0m")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.output(TRIG, False)
time.sleep(2)

# while True:
# print("Die Messung wurde gestartet!")
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
        time.sleep(5)
        GPIO.output(LED_PIN, GPIO.LOW)
    elif (distanz < 25):
        print("\033[93mDie gemessene Distanz beträgt\033[0m", distanz, "cm!")
        GPIO.output(LED_PIN2, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(LED_PIN2, GPIO.LOW)
    else:
        print("\033[92mDer Distanz ist ausreichend\033[0m", distanz, "cm!")
    time.sleep(5)
