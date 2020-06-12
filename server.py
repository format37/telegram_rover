#!/usr/bin/env python3
#Adafruit PWM
from board import SCL, SDA
import busio

#from Adafruit_PCA9685 import PCA9685
import Adafruit_PCA9685

import RPi.GPIO as gpio

import time
#from adafruit_servokit import ServoKit

def track(pwm,channel,power):
	pwm.set_pwm(channel, 0, int(4000*power/100))

pwm = Adafruit_PCA9685.PCA9685()

track(pwm,0,100)
track(pwm,1,100)
time.sleep(3)
track(pwm,0,50)
track(pwm,1,50)
time.sleep(3)
track(pwm,0,0)
track(pwm,1,0)

'''
channel = 0
pulse = 3000 #4k max
pwm.set_pwm(channel, 0, pulse)

channel = 1
pulse = 3000 #4k max
pwm.set_pwm(channel, 0, pulse)
'''

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
'''
kit = ServoKit(channels=16)
 
kit.servo[0].angle = 180
kit.continuous_servo[1].throttle = 1
time.sleep(1)
kit.continuous_servo[1].throttle = -1
time.sleep(1)
kit.servo[0].angle = 0
kit.continuous_servo[1].throttle = 0
'''

'''
i2c_bus = busio.I2C(SCL, SDA)
pca = [
	PCA9685(i2c_bus),
	#PCA9685(i2c_bus,address=0x41)
	]
frequency = 1*2300
direction = 1*0xffff
for i in range(0,len(pca)):
	pca[i].frequency = 60
	pca[i].channels[0].duty_cycle = 0
	pca[i].channels[1].duty_cycle = 0xffff
	
print('start')
track=0
pca[track].frequency = int(frequency)
#pca[track].channels[1].duty_cycle = int(direction)
pca[track].channels[0].duty_cycle = 0x7fff  #go
'''