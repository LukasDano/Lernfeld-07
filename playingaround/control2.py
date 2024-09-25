import RPi.GPIO as GPIO
import time
import random

# GPIO-Nummerierung (BCM)
GPIO.setmode(GPIO.BCM)


def useGivenLED(led_pin):
    # Setup des Pins als Ausgang
    GPIO.setup(led_pin, GPIO.OUT)

    # Test: LED an für 5 Sekunden
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.5)

    # LED aus
    GPIO.output(led_pin, GPIO.LOW)


def useLEDPRO(operand):
    switch = {
        1: lambda: useGivenLED(17),
        2: lambda: useGivenLED(27),
        3: lambda: useGivenLED(18),
    }

    # Standardwert, falls der Schlüssel nicht im Wörterbuch vorhanden ist
    return switch.get(operand, lambda: "Unbekannter Fall")()


for i in range(50):
    # useGivenLED(17)
    # useGivenLED(27)
    useLEDPRO(random.randint(1, 3))

# GPIO-Säuberung
GPIO.cleanup()
