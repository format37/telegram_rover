import telebot
import os

def send_to_telegram():
	with open('/home/pi/telegram_rover/token.key','r') as file:
		MAIN_API_TOKEN=file.read().replace('\n', '')
		file.close()
	main_bot = telebot.TeleBot(MAIN_API_TOKEN)
	video_file = open('/home/pi/telegram_rover/capture/mp4/out.mp4', 'rb')
	main_bot.send_video('-384403215', video_file,timeout=10)
	

script_path = '/home/pi/telegram_rover/capture/'
cmd = ' -force-cat'
for root, subdirs, files in os.walk(script_path+'h264/'):
	for filename in files:
		cmd+=' -cat '+script_path+'h264/'filename
cmd+=' '+script_path+'mp4/out.mp4'
print(cmd)
MyOut = subprocess.Popen(
['MP4Box', cmd],
stdout=subprocess.PIPE, 
stderr=subprocess.STDOUT)
stdout,stderr = MyOut.communicate()		
print('k')