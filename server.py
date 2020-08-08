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
import subprocess
import datetime

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
	
	# ir-cut enable
	ir_cut	= LED(25)
	ir_cut.on()
	time.sleep(0.6)
	
	# voltmeter
	SHUNT_OHMS = 0.1
	ina = INA219(SHUNT_OHMS)
	ina.configure()	
	annotate = str(speed)+" x "+str(int(delay))+" # "+str(track_left)+" : "+str(track_right)+" ( "+str(ina.voltage())+" v )"
	
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
	time.sleep(delay)
	
	# stop
	track(pca,track_free,track_dir,channel=0,direction=0)
	track(pca,track_free,track_dir,channel=1,direction=0)
	
	# video stop
	camera.stop_recording()
	camera.stop_preview()
	camera.close()
	ir_cut.off()
	
def video_send_to_telegram(script_path):
	with open('/home/pi/telegram_rover/token.key','r') as file:
		MAIN_API_TOKEN=file.read().replace('\n', '')
		file.close()
	main_bot = telebot.TeleBot(MAIN_API_TOKEN)
	video_file = open(script_path+'/mp4/out.mp4', 'rb')
	main_bot.send_video('-384403215', video_file,timeout=600)
	
def viceo_convert(script_path):
	mp4_files = []
	h264_files = []
	file_number = 0
	for root, subdirs, files in os.walk(script_path+'h264/'):
		for filename in sorted(files):
			mp4_filepath = script_path+'mp4/out'+str(file_number)+'.mp4'
			cmd = [ 'ffmpeg',
						'-framerate', '24',
						'-i',
						script_path+'h264/'+filename,
						'-c','copy',
						mp4_filepath
				  ]
			ffmpeg = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
			out, err = ffmpeg.communicate()
			mp4_files.append(mp4_filepath)
			print(mp4_filepath)
			h264_files.append(script_path+'h264/'+filename)
			print(filename)
			file_number+=1
	return h264_files,mp4_files

def video_merge(script_path,mp4_files):
	cmd = [ 'MP4Box','-force-cat']
	for full_path in mp4_files:
		cmd.append('-cat')
		cmd.append(full_path)
	cmd.append(script_path+'mp4/out.mp4')
	print(cmd)
	MP4Box = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
	out, err = MP4Box.communicate()

def video_delete_files(script_path,h264_files,mp4_files):	
	mp4_files.append(script_path+'mp4/out.mp4')
	for full_path in mp4_files:
		os.unlink(full_path)
	for full_path in h264_files:
		os.unlink(full_path)
	
async def call_photo(request):
	SCRIPT_PATH = '/home/pi/telegram_rover/'
	MyOut = subprocess.Popen(
	['python3', SCRIPT_PATH+'photo.py','0'],
	stdout=subprocess.PIPE, 
	stderr=subprocess.STDOUT)
	stdout,stderr = MyOut.communicate()		
	return web.Response(text='ok',content_type="text/html")

async def call_photo_night(request):
	SCRIPT_PATH = '/home/pi/telegram_rover/'
	MyOut = subprocess.Popen(
	['python3', SCRIPT_PATH+'photo.py','1'],
	stdout=subprocess.PIPE, 
	stderr=subprocess.STDOUT)
	stdout,stderr = MyOut.communicate()		
	return web.Response(text='ok',content_type="text/html")

async def call_video(request):
	'''
	SCRIPT_PATH = '/home/pi/telegram_rover/capture/'
	MyOut = subprocess.Popen(
	['python3', SCRIPT_PATH+'send_video.py'],
	stdout=subprocess.PIPE, 
	stderr=subprocess.STDOUT)
	stdout,stderr = MyOut.communicate()		
	'''
	script_path = '/home/pi/telegram_rover/capture/'
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
