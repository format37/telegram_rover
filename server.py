#!/usr/bin/env python3
from gpiozero import LED
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

import time

def track(pca,t_free,t_dir,channel,direction):
	if direction==0:
		t_free[channel].on()#free
		pca.channels[channel].duty_cycle = 0 #stop
	else:
		t_free[channel].off()#lock
		pca.channels[channel].duty_cycle = 0x7fff #go
		
	if channel==0:
		if direction ==-1:
			t_dir[channel].on()#back			
		if direction == 1:
			t_dir[channel].off()#front
	if channel==1:
		if direction ==-1:
			t_dir[channel].off()#back
		if direction == 1:
			t_dir[channel].on()#front

print('init')
track_power	= LED(23)
track_free	= [LED(27),LED(17)]
track_dir	= [LED(24),LED(22)]

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
frequency	= 900 #speed 100-2300
pca.frequency=frequency
pca.channels[0].duty_cycle = 0x7fff #go
pca.channels[1].duty_cycle = 0x7fff #go

'''
print('back')
track(pca,track_free,track_dir,channel=0,direction=-1)
track(pca,track_free,track_dir,channel=1,direction=-1)
time.sleep(6)
'''
print('front')
track(pca,track_free,track_dir,channel=0,direction=1)
track(pca,track_free,track_dir,channel=1,direction=1)
time.sleep(1)

'''
print('front')
track(pca,track_free,track_dir,channel=0,direction=1)
track(pca,track_free,track_dir,channel=1,direction=1)
time.sleep(3)

print('back')
track(pca,track_free,track_dir,channel=0,direction=-1)
track(pca,track_free,track_dir,channel=1,direction=-1)
time.sleep(3)

print('stop')
track(pca,track_free,track_dir,channel=0,direction=0)
track(pca,track_free,track_dir,channel=1,direction=0)
time.sleep(3)

print('left')
track(pca,track_free,track_dir,channel=0,direction=-1)
track(pca,track_free,track_dir,channel=1,direction=1)
time.sleep(3)

print('right')
track(pca,track_free,track_dir,channel=0,direction=1)
track(pca,track_free,track_dir,channel=1,direction=-1)
time.sleep(3)
'''
print('stop')
track(pca,track_free,track_dir,channel=0,direction=0)
track(pca,track_free,track_dir,channel=1,direction=0)

while(True):
	time.sleep(1)
	pass