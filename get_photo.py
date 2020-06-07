from picamera import PiCamera
import time
a=1920
b=1920
filepath='image.jpg'
camera = PiCamera()
#camera.rotation=180
camera.resolution = (int(a), int(b))#1920, 1080
camera.start_preview()
time.sleep(1)
camera.capture(filepath)
camera.stop_preview()
camera.close()