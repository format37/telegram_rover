import telebot
import os

def send_to_telegram():
	with open('/home/pi/telegram_rover/token.key','r') as file:
		MAIN_API_TOKEN=file.read().replace('\n', '')
		file.close()
	main_bot = telebot.TeleBot(MAIN_API_TOKEN)
	video_file = open('/home/pi/telegram_rover/capture/mp4/out.mp4', 'rb')
	main_bot.send_video('-384403215', video_file,timeout=10)
	
def convert():
	#file_date=filedate()
	#files_removed_count=0
	for root, subdirs, files in os.walk('/home/pi/telegram_rover/capture/h264/'):
		for filename in files:
			print(filename)
	print('k')
	
convert()
'''
list_file_path = os.path.join(root, 'my-directory-list.txt')
with open(list_file_path, 'wb') as list_file:
	log_message="Processing "+str(len(files))+" files in directory: "+list_file_path
	print(log_message)
	#send_to_telegram(chat,log_message)
	bar = progressbar.ProgressBar(maxval=len(files), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	i=0
	bar.start()
	for filename in files:

		if ".jpg" in filename:
			#print(filename)
			file_date.update(filename)
			file_path = os.path.join(root, filename)

			#time_difference=(date_current-datetime.fromtimestamp( os.path.getctime(file_path) )).total_seconds()
			#day_difference=int(time_difference/60/60/24)
			time_difference=date_current-file_date.dateFormat()
			day_difference=int(time_difference.total_seconds()/60/60/24)

			if day_difference>life_day_lenght:
				os.remove(file_path)
				files_removed_count+=1
			#else:
			#	print("New file "+str(time_difference)+": ("+str(day_difference)+"<="+str(life_day_lenght)+"): "+file_path)
		bar.update(i+1)
		i=i+1;
	bar.finish()
	log_message="Removed by file system: "+str(files_removed_count)+" files"
	print(log_message)
	#send_to_telegram(chat,log_message)
	files_removed_count=0
'''