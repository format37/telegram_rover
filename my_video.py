from picamera import PiCamera
import telebot
import os
import subprocess
#from telebot import apihelper

def delete_first(script_path,files_to_live_count):
	current_file_number = 0
	for root, subdirs, files in os.walk(script_path+'h264/'):
		for filename in sorted(files, reverse=True):
			if current_file_number>=files_to_live_count:
				print('unlink: ' + filename)
				os.unlink(script_path+'h264/' + filename)
			else:
				print("don't touch: " + filename)
			current_file_number+=1
			
def video_delete_all(script_path):	
	for root, subdirs, files in os.walk(script_path+'h264/'):
		for filename in files:
			os.unlink(script_path+'h264/' + filename)
	for root, subdirs, files in os.walk(script_path+'mp4/'):
		for filename in files:
			os.unlink(script_path+'mp4/' + filename)

def video_send_to_telegram(script_path):
	with open('/home/pi/telegram_rover/token.key','r') as file:
		MAIN_API_TOKEN=file.read().replace('\n', '')
		file.close()
	main_bot = telebot.TeleBot(MAIN_API_TOKEN)
	#apihelper.proxy = {'https': 'socks5://telegram.vpn.net:55555'}
	video_file = open(script_path+'mp4/out.mp4', 'rb')
	main_bot.send_video('-384403215', video_file,timeout=12000)

def video_convert(script_path):
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
			if(err) :
				print('error',err)
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
	if(err) :
		print('error',err)

def video_delete_files(script_path,h264_files,mp4_files):	
	mp4_files.append(script_path+'mp4/out.mp4')
	for full_path in mp4_files:
		os.unlink(full_path)
	for full_path in h264_files:
		os.unlink(full_path)
