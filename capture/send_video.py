import telebot
import os
import subprocess

def send_to_telegram():
	with open('/home/pi/telegram_rover/token.key','r') as file:
		MAIN_API_TOKEN=file.read().replace('\n', '')
		file.close()
	main_bot = telebot.TeleBot(MAIN_API_TOKEN)
	video_file = open('/home/pi/telegram_rover/capture/mp4/out.mp4', 'rb')
	main_bot.send_video('-384403215', video_file,timeout=10)
	
#converting
mp4_files = []
script_path = '/home/pi/telegram_rover/capture/'
for root, subdirs, files in os.walk(script_path+'h264/'):
	for filename in files:
		params = []
		params.append('ffmpeg')
		params.append('-framerate')
		params.append('24')
		params.append('-i')
		params.append(script_path+'h264/'+filename)
		params.append('-c')
		params.append('copy')
		params.append(script_path+'mp4/'+filename[:-5]+'.mp4')
		#cmd = ' -framerate 24 -i '+script_path+'h264/'+filename+' -c copy '+script_path+'mp4/'+filename[:-5]+'.mp4'
		mp4_files.append(script_path+'mp4/'+filename[:-5]+'.mp4')
		#print('ffmpeg'+cmd)
		MyOut = subprocess.Popen(
			[params],
			stdout=subprocess.PIPE, 
			stderr=subprocess.STDOUT
		)
		stdout,stderr = MyOut.communicate()
print('k')