from my_video import video_convert, video_merge, video_send_to_telegram, video_delete_files

script_path = '/home/pi/telegram_rover/capture/'
h264_files,mp4_files = video_convert(script_path)
if len(mp4_files):
	video_merge(script_path, mp4_files)
	video_send_to_telegram(script_path)
	video_delete_files(script_path,h264_files, mp4_files)
print(str(len(mp4_files))+' merged')