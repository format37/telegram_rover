import telebot

with open('/home/pi/telegram_rover/token.key','r') as file:
	MAIN_API_TOKEN=file.read().replace('\n', '')
	file.close()
main_bot = telebot.TeleBot(MAIN_API_TOKEN)
video_file = open('/home/pi/telegram_rover/capture/mp4/out.mp4', 'rb')
main_bot.send_video('-384403215', video_file,timeout=10)
#main_bot.send_video('-384403215', 'https://www.scriptlab.net/telegram/bots/calcubot/help.mp4')