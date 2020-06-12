#!/usr/bin/env python3
from gpiozero import LED
#import Adafruit_PCA9685

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

import time

def track(t_free,t_dir,channel,direction):
	if channel==0:
		if direction ==-1:
			t_free[channel].off()#lock
			t_dir[channel].off()#back
		if direction == 0:
			t_free[channel].on()#free
		if direction == 1:
			t_free[channel].off()#lock
			t_dir[channel].on()#front
	if channel==1:
		if direction ==-1:
			t_free[channel].off()#lock
			t_dir[channel].off()#back
		if direction == 0:
			t_free[channel].on()#free
		if direction == 1:
			t_free[channel].off()#lock
			t_dir[channel].on()#front

print('init')
track_free	= [LED(17),LED(27)]
track_dir	= [LED(24),LED(22)]
track(pwm,track_free,track_dir,channel=0,direction=1)
track(pwm,track_free,track_dir,channel=1,direction=1)

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
#speed	= 0.01
#frequency	= speed*2300
frequency	= 100

pca.frequency = frequency
pca.channels[0].duty_cycle = 0x7fff #go
pca.channels[1].duty_cycle = 0x7fff #go
while(True):
	time.sleep(2)
	frequency+=100
	print(frequency)
	pca.frequency = frequency	

#pca.channels[0].duty_cycle = 0 #stop

'''
led			= LED(23)
track_free	= [LED(17),LED(27)]
track_dir	= [LED(24),LED(22)]
#pwm = Adafruit_PCA9685.PCA9685()


print('init')
led.on()
track(pwm,track_free,track_dir,channel=0,direction=0)
track(pwm,track_free,track_dir,channel=1,direction=0)
#pwm.set_pwm_freq(15000-5000)
#pwm.set_pwm(0, 3000)
#pwm.set_pwm(1, 3000)
#frequency = 100*2300
#pwm[0].frequency = int(frequency)
#pwm[1].frequency = int(frequency)
#pwm.channels[0].duty_cycle = 0x7fff
#pwm.channels[1].duty_cycle = 0x7fff
						
print('front')
track(pwm,track_free,track_dir,channel=0,direction=1)
track(pwm,track_free,track_dir,channel=1,direction=1)
time.sleep(3)
print('back')
track(pwm,track_free,track_dir,channel=0,direction=-1)
track(pwm,track_free,track_dir,channel=1,direction=-1)
time.sleep(3)

print('disable')
track(pwm,track_free,track_dir,channel=0,direction=0)
track(pwm,track_free,track_dir,channel=1,direction=0)
while(True):
	pass
'''