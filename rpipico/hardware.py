import utime
from machine import Pin

led_onboard = Pin(25, Pin.OUT)

while True:
    led_onboard.value(1)
    utime.sleep(0.1)
    led_onboard.value(0)
    utime.sleep(0.3)