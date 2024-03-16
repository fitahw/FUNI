from tkinter import INSERT
from yt_dlp.utils import download_range_func
from datetime import datetime
import yt_dlp
import os
import subprocess
import ffmpeg
import multitasking
import json

@multitasking.task
def clipper(OutT, ClipT, pathT):
	print("ass")
	if pathT.get("1.0","end -1 chars") == "":
		OutT.insert(INSERT, 'SPECIFY PATH BEFORE DOWNLOADING!!!\n')
	ClipT.tag_add("download", "1.0", "6.0")
	ClipT.tag_config("download", background="green")

	info = json.load(open("clips.json", "r"))
	url = info[0]['URL']
	time1 = int(info[0]['START'])
	time2 = int(info[0]['END'])

	with yt_dlp.YoutubeDL() as ydl:
		info_dict = ydl.extract_info(url, download=False)
		filename = info_dict.get('title', None)
	
	path = f'{pathT.get("1.0","end -1 chars")}/{filename}_{time1}'
	del info[0]
	if len(info) == 0:
		print("NO CLIPS IN MEMORY")
	json.dump(info, open('clips.json', 'w'))
	# CLIP DOWNLOAD OPTIONS
	ydl_opts = {
	'outtmpl': path,
	'format': 'bv+ba',
	'download_ranges': download_range_func(None, [(time1, time2)]),
	'force_keyframes_at_cuts' : True,
	'postprocessors': [{
	'key': 'FFmpegVideoConvertor',
	'preferedformat': 'mp4'
	}]
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		OutT.insert(INSERT, f'({datetime.now().strftime("%H:%M:%S")}) DOWNLOADING CLIP {filename}_{time1}...\n')
		try:
			ydl.download(url)
		except:
			OutT.insert(INSERT, f'({datetime.now().strftime("%H:%M:%S")}) STARTING ALTERNATE DOWNLOAD...\n')

			# VIDEO ONLY DOWNLOAD OPTIONS
			ydl_opts_v = {
				'outtmpl': f'{filename}_{time1}_v.mp4',
				'format': '299',
				'download_ranges': download_range_func(None, [(time1, time2)]),
				'force_keyframes_at_cuts' : True,
				'postprocessors': [{
				'key': 'FFmpegVideoConvertor',
				'preferedformat': 'mp4'
				}]
				}

			# AUDIO ONLY DOWNLOAD OPTIONS
			ydl_opts_a = {
				'outtmpl': f'{filename}_{time1}_a',
				'format': '251',
				'download_ranges': download_range_func(None, [(time1, time2)]),
				'force_keyframes_at_cuts' : True,
				'postprocessors': [{
				'key': 'FFmpegExtractAudio'
				},{
				'key': 'FFmpegFixupM4a'}]
				}
			yt_dlp.YoutubeDL(ydl_opts_v).download(url)
			yt_dlp.YoutubeDL(ydl_opts_a).download(url)

			commannd = f"ffmpeg -i {path + '_v.mp4'} -i {path + '_a.m4a'} -c:v copy -c copy {path + '.mp4'}"
			subprocess.call(commannd,shell=True, cwd=f'/')

			os.remove(path + '_v.mp4')
			os.remove(path + '_a.m4a')
		OutT.insert(INSERT, f'({datetime.now().strftime("%H:%M:%S")}) DOWNLOAD SUCCESSFUL\n')

	ClipT.delete('1.0', '6.0')
	print("Downloaded")