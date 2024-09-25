import RPi.GPIO as GPIO
import time

# GPIO-Nummerierung (BCM)
GPIO.setmode(GPIO.BCM)

# Pin, an dem die LED angeschlossen ist
LED_PIN = 17

# Setup des Pins als Ausgang
GPIO.setup(LED_PIN, GPIO.OUT)

# Test: LED an für 5 Sekunden
GPIO.output(LED_PIN, GPIO.HIGH)
print("LED an")
time.sleep(5)

# LED aus
GPIO.output(LED_PIN, GPIO.LOW)
print("LED aus")

# GPIO-Säuberung
GPIO.cleanup()

while 1 == 1:
    print("");
