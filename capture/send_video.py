import telebot

with open('/home/pi/telegram_rover/token.key','r') as file:
	MAIN_API_TOKEN=file.read().replace('\n', '')
	file.close()
main_bot = telebot.TeleBot(MAIN_API_TOKEN)
main_bot.send_video('-384403215', '/home/pi/telegram_rover/capture/mp4/out.mp4')