from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from datetime import datetime
from yt_dlp.utils import download_range_func
import os
import subprocess
import json
import yt_dlp
import ffmpeg
import multitasking

@multitasking.task
def open_text_file(*args):
	path = fd.askdirectory(initialdir="Downloads", mustexist=False)
	pathT.delete('1.0', '3.0')
	pathT.insert('1.0', path)

@multitasking.task
def inputter(*args):
	time1 = MinTime1.get()*60+SecTime1.get()
	time2 = MinTime2.get()*60+SecTime2.get()
	try:
		json.dump(json.load(open('clips.json', 'r')) + [{'URL': url.get(), 'START': time1, 'END': time2}], open('clips.json', 'w'), indent=3)
	except:
		json.dump([], open('clips.json', 'w'))
		json.dump(json.load(open('clips.json', 'r')) + [{'URL': url.get(), 'START': time1, 'END': time2}], open('clips.json', 'w'), indent=3)
	ClipT.insert(END, f'\nURL: {url.get()}\nSTART: {time1}\nEND: {time2}\n')
	OutT.insert(INSERT, f'({datetime.now().strftime("%H:%M:%S")}) WRITE DONE\n')

@multitasking.task
def clipper(*args):
	if pathT.get("1.0","end -1 chars") == "":
		OutT.insert(INSERT, 'SPECIFY PATH BEFORE DOWNLOADING!!!\n')
		return
	info = json.load(open("clips.json", "r"))
	ClipT.tag_add("download", "1.0", "6.0")
	ClipT.tag_config("download", background="green")
	url = info[0]['URL']
	time1 = int(info[0]['START'])
	time2 = int(info[0]['END'])

	with yt_dlp.YoutubeDL() as ydl:
		info_dict = ydl.extract_info(url, download=False)
		filename = info_dict.get('title', None)
	
	del info[0]
	if len(info) == 0:
		print("NO CLIPS IN MEMORY")
		json.dump(info, open('clips.json', 'w'))
	else:
		json.dump(info, open('clips.json', 'w'))

	ydl_opts = {
	'outtmpl': f'{pathT.get("1.0","end -1 chars")}/{filename}_{time1}',
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
			file = ydl.download(url)
		except:
			OutT.insert(INSERT, f'({datetime.now().strftime("%H:%M:%S")}) STARTING ALTERNATE DOWNLOAD...\n')
			ydl_opts_v = {
				'outtmpl': f'{filename}_{time1}_v.mp4',
				'format': '312',
				'download_ranges': download_range_func(None, [(time1, time2)]),
				'force_keyframes_at_cuts' : True,
				'postprocessors': [{
				'key': 'FFmpegVideoConvertor',
				'preferedformat': 'mp4'
				}]
				}

			ydl_opts_a = {
				'outtmpl': f'{filename}_{time1}_a',
				'format': '22',
				'download_ranges': download_range_func(None, [(time1, time2)]),
				'force_keyframes_at_cuts' : True,
				'postprocessors': [{
				'key': 'FFmpegExtractAudio'
				},{
				'key': 'FFmpegFixupM4a'}]
				}
			ydlV = yt_dlp.YoutubeDL(ydl_opts_v)
			ydlA = yt_dlp.YoutubeDL(ydl_opts_a)
			file = ydlV.download(url)
			file2 = ydlA.download(url)
			video_path = f'{pathT.get("1.0","end -1 chars")}/{filename}_{time1}_v.mp4'
			audio_path = f'{pathT.get("1.0","end -1 chars")}/{filename}_{time1}_a.m4a'
			output_path = f'{pathT.get("1.0","end -1 chars")}/{filename}_{time1}.mp4'
			ffmpeg_path = '/'
			commannd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c copy {output_path}  && rm {video_path}"
			subprocess.call(commannd,shell=True, cwd=f'{ffmpeg_path}')
			os.remove(video_path)
			os.remove(audio_path)
		OutT.insert(INSERT, f'({datetime.now().strftime("%H:%M:%S")}) DOWNLOAD SUCCESSFUL\n')

	ClipT.delete('1.0', '6.0')
	print("Downloaded")

root = Tk()
root.title("YTClipper")
root.configure(cursor=("@gugu.ani"))
root.resizable(0,0)

ttk.Label(root, text="Clip Download Path:").grid(column=0, row=0)
open_button = ttk.Button(root, text='Select Path', command=open_text_file, width=10).grid(column=3, row=0, sticky=E, pady=2)
pathT = Text(root, height=1, width=25)
pathT.grid(column=1, row=0, columnspan=2, sticky=W)

url = StringVar()
ttk.Label(root, text="URL:").grid(column=0, row=1)
url_entry = ttk.Entry(root, width=50, textvariable=url)
url_entry.grid(column=1, row=1, columnspan=3, sticky=W)

MinTime1 = IntVar()
SecTime1 = IntVar()
ttk.Label(root, text='Start Time [min|sec]').grid(column=0, row=2, pady=5)
MinTime1_entry = ttk.Entry(root, width=7, textvariable=MinTime1)
MinTime1_entry.grid(column=1, row=2, padx=1, sticky=W)
SecTime1_entry = ttk.Entry(root, width=7, textvariable=SecTime1)
SecTime1_entry.grid(column=2, row=2)

MinTime2 = IntVar()
SecTime2 = IntVar()
ttk.Label(root, text='End Time [min|sec]').grid(column=0, row=3)
MinTime2_entry = ttk.Entry(root, width=7, textvariable=MinTime2)
MinTime2_entry.grid(column=1, row=3, padx=1, sticky=W)
SecTime2_entry = ttk.Entry(root, width=7, textvariable=SecTime2)
SecTime2_entry.grid(column=2, row=3)

OutT = Text(root, width=28, height=7, bd=1, padx=4, wrap=WORD)
ClipT = Text(root, width=40, height=10, wrap=WORD)
OutT.grid(column=0, row=6, columnspan=1, sticky=W)
ClipT.grid(column=1,row=6, columnspan=4, sticky=E)

ttk.Button(root, text="Input", command=inputter).grid(column=3, row=4, pady=4, sticky=E)

ttk.Button(root, text="Download First", command=clipper).grid(column=2, row=4)

#TODO
ttk.Button(root, text="Download All").grid(column=1, row=4, sticky=W)

try:
	printClips = json.load(open('clips.json', 'r'))
	for clip in printClips:
		ClipT.insert(END, f'\nURL:{clip["URL"]}\nSTART:{clip["START"]}\nEND:{clip["END"]}\n')
except:
	OutT.insert(INSERT, f'({datetime.now().strftime("%H:%M:%S")}) NO CLIPS FOUND\n')
url_entry.focus()
root.bind("<Return>", inputter)

root.mainloop()