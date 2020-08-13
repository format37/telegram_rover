from adafruit_pca9685 import PCA9685
from ina219 import INA219
import time

def send_report(voltage):
	with open('/home/pi/telegram_rover/token.key','r') as file:
		MAIN_API_TOKEN=file.read().replace('\n', '')
		file.close()
	main_bot = telebot.TeleBot(MAIN_API_TOKEN)
	main_bot.send_message('-384403215', 'low voltage: '+str(voltage)+' v. Moving forward..')

SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS)
ina.configure()		
while True:	
	print(str(round(ina.voltage(),2))+" v. ")
	time.sleep(0.5)
	