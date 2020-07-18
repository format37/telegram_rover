import time
import resource
import sys
from gpiozero import LED

try:
	night_led = LED(8)
	led_time = sys.argv[1]
	res_limits = resource.getrusage(resource.RUSAGE_SELF)
	resource.setrlimit(resource.RLIMIT_CPU, (1, led_time+1))		
	night_led.on()
	time.sleep(led_time)
	night_led.off()
	
except Exception as e:
	print(e)
