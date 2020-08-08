import time
import sys
from gpiozero import LED
from aiohttp import web
import asyncio
from picamera import PiCamera
import telebot
from ina219 import INA219

ir_cut	= LED(25)
nigth_led = LED(8)
nigth_mode = int(sys.argv[1]) #0 or 1

if nigth_mode:
	ir_cut.off()
	nigth_led.on()
else:
	ir_cut.on()
	nigth_led.off()

# get photo
a=1280 #600 #2560
b=720 #600 #1920
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

telebot.apihelper.READ_TIMEOUT = 15
bot = telebot.TeleBot(API_TOKEN)
data_file = open('/home/pi/telegram_rover/image.jpg', 'rb')

SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS)
ina.configure()	
print('sending photo..')
bot.send_photo( '-384403215', data_file, caption = str(ina.voltage())+" v" )		
