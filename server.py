#!/usr/bin/env python3
from gpiozero import LED
import Adafruit_PCA9685
import time

led = LED(23)
track_free=[LED(17),LED(27)]
pwm = Adafruit_PCA9685.PCA9685()

def track(pwm,t_free,channel,direction):
	if channel==0:
		if direction ==-1:
			t_free[channel].off()#lock
		if direction == 0:
			t_free[channel].on()#free
		if direction == 1:
			t_free[channel].off()#lock
	if channel==1:
		if direction ==-1:
			t_free[channel].off()#lock
		if direction == 0:
			t_free[channel].on()#free
		if direction == 1:
			t_free[channel].off()#lock

print('init')
track(pwm,track_free,channel=0,direction=0)
track(pwm,track_free,channel=1,direction=0)
pwm.set_pwm(channel, 0, 4000)
						
print('start')
track(pwm,track_free,channel=0,direction=1)
track(pwm,track_free,channel=1,direction=1)
time.sleep(3)

print('disable')
track(pwm,track_free,channel=0,direction=0)
track(pwm,track_free,channel=1,direction=0)
while(True):
	pass