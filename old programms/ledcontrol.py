import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

LED_PIN = 17

GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, GPIO.HIGH)
print("LED an")
time.sleep(5)

GPIO.output(LED_PIN, GPIO.LOW)
print("LED aus")

GPIO.cleanup()
