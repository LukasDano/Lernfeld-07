import RPi.GPIO as GPIO
import time

# GPIO-Nummerierung (BCM)
GPIO.setmode(GPIO.BCM)


def turnOnLED1():
    # Pin, an dem die LED angeschlossen ist
    led_pin = 17

    # Setup des Pins als Ausgang
    GPIO.setup(led_pin, GPIO.OUT)

    # Test: LED an für 5 Sekunden
    GPIO.output(led_pin, GPIO.HIGH)
   # print("LED1 an")
    time.sleep(0.5)

    # LED aus
    GPIO.output(led_pin, GPIO.LOW)
    #print("LED1 aus")


def turnOnLED2():
    # Pin, an dem die LED angeschlossen ist
    led_pin = 27

    # Setup des Pins als Ausgang
    GPIO.setup(led_pin, GPIO.OUT)

    # Test: LED an für 5 Sekunden
    GPIO.output(led_pin, GPIO.HIGH)
    #print("LED2 an")
    time.sleep(0.5)

    # LED aus
    GPIO.output(led_pin, GPIO.LOW)
    #print("LED2 aus")


for i in range(42):
    turnOnLED1()
    turnOnLED2()


# GPIO-Säuberung
GPIO.cleanup()
