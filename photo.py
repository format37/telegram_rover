import time
import resource
import sys
from gpiozero import LED
#import telebot
#from ina219 import INA219
#from picamera import PiCamera

from aiohttp import web
import asyncio
from picamera import PiCamera
import telebot
from ina219 import INA219
import time
import subprocess

#try:
ir_cut	= LED(25)
nigth_led = LED(8)
nigth_mode = int(sys.argv[1]) #0 or 1
#res_limits = resource.getrusage(resource.RUSAGE_SELF)
#resource.setrlimit(resource.RLIMIT_CPU, (10, 10))

ir_cut.on()
nigth_led.off()

# get photo
a=1920
b=1920
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

telebot.apihelper.READ_TIMEOUT = 5
bot = telebot.TeleBot(API_TOKEN)
data_file = open('/home/pi/telegram_rover/image.jpg', 'rb')

SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS)
ina.configure()	

bot.send_photo( '-384403215', data_file, caption = str(ina.voltage())+" v" )		
	
#except Exception as e:
#	print(e)