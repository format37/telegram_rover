from ina219 import INA219
import time
import telebot
from gpiozero import LED
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

def send_report(message):
	with open('/home/pi/telegram_rover/token.key','r') as file:
		MAIN_API_TOKEN=file.read().replace('\n', '')
		file.close()
	main_bot = telebot.TeleBot(MAIN_API_TOKEN)
	main_bot.send_message('-384403215', message)
	
def move_forward():
	
	frequency	= 2300
	
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
	track(pca,track_free,track_dir,channel=0,direction=1)
	track(pca,track_free,track_dir,channel=1,direction=1)	
	time.sleep(2)
	
	# stop
	track(pca,track_free,track_dir,channel=0,direction=0)
	track(pca,track_free,track_dir,channel=1,direction=0)

with open('/home/pi/telegram_rover/charge_mode.key','r') as file:
	charge_mode=int(file.read().replace('\n', ''))
	file.close()	

if charge_mode:
	SHUNT_OHMS = 0.1
	ina = INA219(SHUNT_OHMS)
	ina.configure()		
	voltage_current = ina.voltage()
	if voltage_current<13:
		send_report('low voltage: '+str(voltage_current)+' v. Moving forward..')
		move_forward()
		time.sleep(1)
		voltage_current = ina.voltage()
		send_report('Voltage current: '+str(voltage_current))