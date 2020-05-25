#!/usr/bin/env python3
#Adafruit PWM
from board import SCL, SDA
import busio
#from adafruit_pca9685 import PCA9685
from Adafruit_PCA9685 import PCA9685
import RPi.GPIO as gpio

i2c_bus = busio.I2C(SCL, SDA)
pca = [
	PCA9685(i2c_bus,address=0x40),
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