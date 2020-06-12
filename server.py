#!/usr/bin/env python3
#from board import SCL, SDA
#import busio
from gpiozero import LED
import Adafruit_PCA9685
#import RPi.GPIO as gpio
import time

def track(pwm,channel,power):
	print(channel,int(4000*power/100))
	pwm.set_pwm(channel, 0, int(4000*power/100))
	
led = LED(23)
tracks=[LED(17),LED(27)]
pwm = Adafruit_PCA9685.PCA9685()

led.off()
tracks[0].on()
tracks[1].on()
track(pwm,0,100)
track(pwm,1,100)
time.sleep(3)
#track(pwm,0,0)
#track(pwm,1,0)
tracks[0].off()
tracks[1].off()