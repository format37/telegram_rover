#!/usr/bin/env python3
# rover
from gpiozero import LED
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
# server
from aiohttp import web
import asyncio

import time

PORT = '8823'

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

def call_move(request):
	
	delay		= float(request.rel_url.query['delay'])
	track_left	= int(request.rel_url.query['track_left'])
	track_right	= int(request.rel_url.query['track_right'])
	frequency	= int( request.rel_url.query['speed']*2300/100 )
	frequency	= frequency if frequency>100 else 100
	
	print('init')
	track_power	= LED(23)
	track_free	= [LED(27),LED(17)]
	track_dir	= [LED(24),LED(22)]

	i2c_bus = busio.I2C(SCL, SDA)
	pca = PCA9685(i2c_bus)
	#frequency	= 900 #speed 100-2300
	pca.frequency=frequency
	pca.channels[0].duty_cycle = 0x7fff #go
	pca.channels[1].duty_cycle = 0x7fff #go

	
	#print('back')
	
	track(pca,track_free,track_dir,channel=0,direction=track_left)
	track(pca,track_free,track_dir,channel=1,direction=track_right)
	time.sleep(delay)
	
	'''
	print('front')
	track(pca,track_free,track_dir,channel=0,direction=1)
	track(pca,track_free,track_dir,channel=1,direction=1)
	time.sleep(1)

	
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
'''
	while(True):
		time.sleep(1)
		pass
	'''

async def call_check(request):
	return web.Response(text='ok',content_type="text/html")

app = web.Application()
app.router.add_route('GET', '/check', call_check)
app.router.add_route('GET', '/move', call_move)

# Start aiohttp server
web.run_app(
    app,
    host='172.27.220.5',
    port=PORT,
)