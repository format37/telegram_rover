import telebot
import requests

def bot_init(WEBHOOK_HOST,WEBHOOK_PORT,WEBHOOK_SSL_CERT, SCRIPT_PATH):

	with open(SCRIPT_PATH+'token.key','r') as file:
		API_TOKEN=file.read().replace('\n', '')
		file.close()
	bot = telebot.TeleBot(API_TOKEN)

	WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
	WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)

	# Remove webhook, it fails sometimes the set if there is a previous webhook
	bot.remove_webhook()

	# Set webhook
	wh_res = bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,certificate=open(WEBHOOK_SSL_CERT, 'r'))
	print('rover webhook set',wh_res)
	print(WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

	return bot

def move_cmd(user_id,cmd):
	god_mode	= user_id == 106129214
	if god_mode:
		url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd
		return 'ok cmd '+str(requests.get(url).text)
	else:
		return "unavailable for. u"

def move_f(user_id,delay,speed):
	god_mode	= user_id == 106129214
	if god_mode:
		cmd 	= 'track_left=1&track_right=1&delay='+str(delay)+'&speed='+str(speed)
		url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd
		return	'ok f '+str(requests.get(url).text)
	else:
		return "unavailable for. u"

	
def move_b(user_id,delay,speed):
	god_mode	= user_id == 106129214
	if god_mode:
		cmd 	= 'track_left=-1&track_right=-1&delay='+str(delay)+'&speed='+str(speed)
		url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd
		return	'ok b '+str(requests.get(url).text)
	else:
		return "unavailable for. u"
	
def move_l(user_id,delay,speed):
	god_mode	= user_id == 106129214
	if god_mode:
		cmd 	= 'track_left=-1&track_right=1&delay='+str(delay)+'&speed='+str(speed)
		url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd
		return	'ok l '+str(requests.get(url).text)
	else:
		return "unavailable for. u"	
		
def move_r(user_id,delay,speed):
	god_mode	= user_id == 106129214
	if god_mode:
		cmd 	= 'track_left=1&track_right=-1&delay='+str(delay)+'&speed='+str(speed)
		url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd		
		return	'ok r '+str(requests.get(url).text)
	else:
		return "unavailable for. u"
	
def rover_photo(user_id):
	god_mode	= user_id == 106129214
	if god_mode:
		url	= "http://95.165.139.53:8823/telegram_rover_photo.php"
		return	'ok p '+requests.get(url).text
	else:
		return "unavailable for. u"

def rover_photo_night(user_id):
	god_mode	= user_id == 106129214
	if god_mode:
		url	= "http://95.165.139.53:8823/telegram_rover_photo_night.php"
		return	'ok n '+requests.get(url).text
	else:
		return "unavailable for. u"
	
def rover_send_video_merged(user_id):
	god_mode	= user_id == 106129214
	if god_mode:
		url	= "http://95.165.139.53:8823/telegram_rover_video.php"
		return	'ok v '+requests.get(url).text
	else:
		return "unavailable for. u"