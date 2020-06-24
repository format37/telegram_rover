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
		requests.get(url)
		#requests.get(url,headers = headers)
		return 'job complete: '+cmd
	else:
		return "unavailable for. u"

	'''
	headers = {
		"Origin": "http://95.165.139.53",
		"Referer": "http://95.165.139.53/",
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
	'''
	#cmd = 'track_left=-1&track_right=-1&delay=5&speed=10'
	url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd
	return	requests.get(url)
	#return	requests.get(url,headers = headers)

def move_f(user_id,delay,speed):
	cmd 	= 'track_left=1&track_right=1&delay='+str(delay)+'&speed='+str(speed)
	url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd
	return	requests.get(url)
	#return	requests.get(url,headers = headers)
	
def move_b(user_id,delay,speed):
	cmd 	= 'track_left=-1&track_right=-1&delay='+str(delay)+'&speed='+str(speed)
	url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd
	return	requests.get(url)
	#return	requests.get(url,headers = headers)
	
def move_l(user_id,delay,speed):
	cmd 	= 'track_left=-1&track_right=1&delay='+str(delay)+'&speed='+str(speed)
	url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd
	return	requests.get(url)
	#return	requests.get(url,headers = headers)
	
def move_r(user_id,delay,speed):
	cmd 	= 'track_left=1&track_right=-1&delay='+str(delay)+'&speed='+str(speed)
	url	= "http://95.165.139.53:8823/telegram_rover.php?"+cmd
	return	requests.get(url)
	#return	requests.get(url,headers = headers)
