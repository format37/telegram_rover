#!/usr/bin/env python3
# rover
from gpiozero import LED
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
# server
from aiohttp import web
import asyncio
from picamera import PiCamera
import time
import telebot

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
	frequency	= int( float(request.rel_url.query['speed'])*2300/100 )
	frequency	= frequency if frequency>100 else 100
	
	# init
	track_power	= LED(23)
	track_free	= [LED(27),LED(17)]
	track_dir	= [LED(24),LED(22)]

	i2c_bus = busio.I2C(SCL, SDA)
	pca = PCA9685(i2c_bus)
	pca.frequency=frequency
	pca.channels[0].duty_cycle = 0x7fff #go
	pca.channels[1].duty_cycle = 0x7fff #go
	
	# move	
	track(pca,track_free,track_dir,channel=0,direction=track_left)
	track(pca,track_free,track_dir,channel=1,direction=track_right)
	time.sleep(delay)
	
	# stop
	track(pca,track_free,track_dir,channel=0,direction=0)
	track(pca,track_free,track_dir,channel=1,direction=0)
	
async def call_photo(request):
	
	# get photo
	a=1920
	b=1920
	#a=640 # 1920
	#b=480 # 1920
	filepath='/home/pi/telegram_rover/image.jpg'
	camera = PiCamera()
	#camera.rotation=180
	camera.resolution = (int(a), int(b))
	camera.start_preview()
	time.sleep(1)
	camera.capture(filepath)
	camera.stop_preview()
	camera.close()
	
	# send to telegram
	with open('/home/pi/telegram_rover/token.key','r') as file:
		API_TOKEN=file.read().replace('\n', '')
		file.close()
	bot = telebot.TeleBot(API_TOKEN)
	data_file = open('/home/pi/telegram_rover/image.jpg', 'rb')
	bot.send_photo('-384403215', data_file)
	
	return web.Response(text='ok',content_type="text/html")

async def call_check(request):
	return web.Response(text='ok',content_type="text/html")

app = web.Application()
app.router.add_route('GET', '/move',	call_move)
app.router.add_route('GET', '/photo',	call_photo)
app.router.add_route('GET', '/check',	call_check)

# send ready
with open('/home/pi/telegram_rover/token.key','r') as file:
	MAIN_API_TOKEN=file.read().replace('\n', '')
	file.close()
main_bot = telebot.TeleBot(MAIN_API_TOKEN)
main_bot.send_message('-384403215', 'ready')

# Start aiohttp server
web.run_app(
    app,
    host='172.27.220.5',
    port=PORT,
)
