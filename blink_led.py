#!/usr/bin/env python
# blink_led.py
# gpio test code for pcduino ( http://www.pcduino.com )
#
import gpio
import time

led_pin = "gpio0"

def delay(ms):
    time.sleep(1.0*ms/1000)

def setup():
    gpio.pinMode(led_pin, gpio.OUTPUT)

def loop():
    while(1):
        gpio.digitalWrite(led_pin, gpio.HIGH)
        delay(200)
	print "prendido"
        gpio.digitalWrite(led_pin, gpio.LOW)
        delay(100)
	print "apagado"

def main():
    setup()
    loop()

main()
