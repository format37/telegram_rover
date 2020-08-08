import telebot
import os
import subprocess
#import sh

def send_to_telegram(script_path):
	with open('/home/pi/telegram_rover/token.key','r') as file:
		MAIN_API_TOKEN=file.read().replace('\n', '')
		file.close()
	main_bot = telebot.TeleBot(MAIN_API_TOKEN)
	video_file = open(script_path+'/mp4/out.mp4', 'rb')
	main_bot.send_video('-384403215', video_file,timeout=600)
	
def convert(script_path):
	mp4_files = []
	h264_files = []
	file_number = 0
	for root, subdirs, files in os.walk(script_path+'h264/'):
		for filename in files:
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

def merge(script_path,mp4_files):
	cmd = [ 'MP4Box','-force-cat']
	for full_path in mp4_files:
		cmd.append('-cat')
		cmd.append(full_path)
	cmd.append(script_path+'mp4/out.mp4')
	print(cmd)
	MP4Box = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
	out, err = MP4Box.communicate()

def delete_files(script_path,h264_files,mp4_files):	
	mp4_files.append(script_path+'mp4/out.mp4')
	for full_path in mp4_files:
		os.unlink(full_path)
	for full_path in h264_files:
		os.unlink(full_path)

script_path = '/home/pi/telegram_rover/capture/'
h264_files,mp4_files = convert(script_path)
merge(script_path, mp4_files)
send_to_telegram(script_path)
delete_files(script_path,h264_files, mp4_files)