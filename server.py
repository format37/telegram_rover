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
import telebot
from ina219 import INA219
import time
import os
import subprocess
import datetime
from my_video import video_convert, video_merge, video_send_to_telegram, video_delete_files, delete_first

PORT = '8823'
#night_led = LED(8)
#night_led.off()


def rover_init():
	# send ready
	with open('/home/pi/telegram_rover/token.key','r') as file:
		MAIN_API_TOKEN=file.read().replace('\n', '')
		file.close()
	main_bot = telebot.TeleBot(MAIN_API_TOKEN)
	main_bot.send_message('-384403215', 'ready')


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
	speed		= int(request.rel_url.query['speed'])
	frequency	= int( float(speed)*2300/100 )
	frequency	= frequency if frequency>100 else 100
	time_spent  = 0
	
	# ir-cut enable
	ir_cut	= LED(25)
	ir_cut.on()
	time.sleep(0.6)
	
	# voltmeter
	SHUNT_OHMS = 0.1
	ina = INA219(SHUNT_OHMS)
	ina.configure()		
	#annotate = str(speed)+" x "+str(int(delay))+" # "+str(track_left)+" : "+str(track_right)+" ( "+str(ina.voltage())+" v )"
	annotate = str(round(ina.voltage(),2))+" v. "+str(round(time_spent,1))+" / "+str(int(delay))
	
	# video start
	camera = PiCamera()
	camera.annotate_text = annotate
	camera.start_preview()	
	filename = 'video_'+(f"{datetime.datetime.now():%Y.%m.%d_%H:%M:%S}")+'.h264'
	camera.start_recording('/home/pi/telegram_rover/capture/h264/'+filename)	
	
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
	while time_spent<delay:
		time.sleep(0.1)
		time_spent+=0.1
		#annotate = str(speed)+" x "+str(time_spent)+" / "+str(int(delay))+" # "+str(track_left)+" : "+str(track_right)+" ( "+str(ina.voltage())+" v )"
		annotate = str(round(ina.voltage(),2))+" v. "+str(round(time_spent,1))+" / "+str(int(delay))
		camera.annotate_text = annotate
	
	# stop
	track(pca,track_free,track_dir,channel=0,direction=0)
	track(pca,track_free,track_dir,channel=1,direction=0)
	
	# video stop
	time.sleep(1)
	camera.stop_recording()
	camera.stop_preview()
	camera.close()
	ir_cut.off()
	
async def call_photo(request):
	night_key = read_night_key()
	SCRIPT_PATH = '/home/pi/telegram_rover/'
	MyOut = subprocess.Popen(
	['python3', SCRIPT_PATH+'photo.py',str(night_key)],
	stdout=subprocess.PIPE, 
	stderr=subprocess.STDOUT)
	stdout,stderr = MyOut.communicate()		
	return web.Response(text='ok',content_type="text/html")

def read_night_key():
	key_path = '/home/pi/telegram_rover/night_vision.key'
	with open(key_path,'r') as file:
		night_key=int(file.read().replace('\n', ''))
		file.close()
	return night_key
		
async def call_photo_night(request):
	'''
	SCRIPT_PATH = '/home/pi/telegram_rover/'
	MyOut = subprocess.Popen(
	['python3', SCRIPT_PATH+'photo.py','1'],
	stdout=subprocess.PIPE, 
	stderr=subprocess.STDOUT)
	stdout,stderr = MyOut.communicate()		
	return web.Response(text='ok',content_type="text/html")
	'''
	# night vision switcher
	night_key = read_night_key()
		
	if night_key:
		answer = 'Night vision: Disabled'
		night_key = 0
	else:
		answer = 'Night vision: Enabled'
		night_key = 1
		
	with open(key_path,'w') as file:
		file.write(str(night_key))
		file.close()
		
	return web.Response(text=answer,content_type="text/html")
	
async def call_video(request):
	script_path = '/home/pi/telegram_rover/capture/'
	delete_first(script_path,20)
	h264_files,mp4_files = video_convert(script_path)
	if len(mp4_files):
		video_merge(script_path, mp4_files)
		video_send_to_telegram(script_path)
		video_delete_files(script_path,h264_files, mp4_files)
	return web.Response(text=str(len(mp4_files))+' merged',content_type="text/html")

async def call_check(request):
	return web.Response(text='ok',content_type="text/html")

rover_init()

app = web.Application()
app.router.add_route('GET', '/move',	call_move)
app.router.add_route('GET', '/photo',	call_photo)
app.router.add_route('GET', '/photo_night',	call_photo_night)
app.router.add_route('GET', '/check',	call_check)
app.router.add_route('GET', '/video',	call_video)

# Start aiohttp server
web.run_app(
    app,
    host='172.27.220.5',
    port=PORT,
)
