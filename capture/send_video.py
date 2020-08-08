import telebot
import os
import subprocess
#import sh

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
		
		#cmd = 'ffmpeg -framerate 24 -i '+script_path+'h264/'+filename+' -c copy '+script_path+'mp4/'+filename[:-5]+'.mp4'
		
		cmd = [ 'ffmpeg',
					'-framerate', '24',
					'-i',
					script_path+'h264/'+filename,
					'-c','copy',
					script_path+'mp4/'+filename[:-5]+'.mp4'
			  ]
		ffmpeg = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
		out, err = ffmpeg.communicate()

		if(err) : print('error',err)
		
		#params = []
		#params.append('ffmpeg')
		#params.append('-framerate 24')
		#params.append('24')
		#params.append('-i')
		#params.append(script_path+'h264/'+filename)
		#params.append('-c')
		#params.append('copy')
		#params.append(script_path+'mp4/'+filename[:-5]+'.mp4')
		
		#cmd = 'ffmpeg -framerate 24 -i '+script_path+'h264/'+filename+' -c copy '+script_path+'mp4/'+filename[:-5]+'.mp4'
		
		mp4_files.append(script_path+'mp4/'+filename[:-5]+'.mp4')
		
		#print('ffmpeg'+cmd)
		#MyOut = subprocess.Popen(
		#	cmd,
		#	stdout=subprocess.PIPE, 
		#	stderr=subprocess.STDOUT
		#)
		#stdout,stderr = MyOut.communicate()
		#for line in stdout:
		#	print(line)
		#process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
		#for line in process.stdout:
		#	print(line)
print('k')