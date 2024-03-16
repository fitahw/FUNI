import tkinter as tk
from tkinter import ttk, Text, StringVar, IntVar, END, INSERT
from tkinter import filedialog as fd
import json
from datetime import datetime

class GUI:
	def __init__(self, Groot):
		# ROOT SETUP
		self.Groot = Groot
		self.Groot.title("YTClipper")
		self.Groot.configure(cursor="@gugu.ani")
		self.Groot.resizable(0, 0)

		# FFMPEG PATH INPUT
		ttk.Label(Groot, text="FFmpeg.exe Path:").grid(column=0, row=0)
		self.pathFF = Text(Groot, height=1, width=25)
		self.pathFF.grid(column=1, row=0, columnspan=2, sticky=tk.W)
		open_button = ttk.Button(Groot, text='Select Path', command=lambda: self.setPath(self.pathFF), width=10)
		open_button.grid(column=3, row=0, sticky=tk.E, pady=2)

		# DOWNLOAD PATH INPUT
		ttk.Label(Groot, text="Clip Download Path:").grid(column=0, row=1)
		self.pathT = Text(Groot, height=1, width=25)
		self.pathT.grid(column=1, row=1, columnspan=2, sticky=tk.W)
		open_button = ttk.Button(Groot, text='Select Path', command=lambda: self.setPath(self.pathT), width=10)
		open_button.grid(column=3, row=1, sticky=tk.E, pady=2)

		# URL INPUT
		self.url = StringVar()
		ttk.Label(Groot, text="URL:").grid(column=0, row=2)
		url_entry = ttk.Entry(Groot, width=50, textvariable=self.url)
		url_entry.grid(column=1, row=2, columnspan=3, sticky=tk.W)

		# BEGIN TIME
		self.MinTime1 = IntVar()
		self.SecTime1 = IntVar()
		ttk.Label(Groot, text='Start Time [min|sec]').grid(column=0, row=3, pady=5)
		MinTime1_entry = ttk.Entry(Groot, width=7, textvariable=self.MinTime1)
		MinTime1_entry.grid(column=1, row=3, padx=1, sticky=tk.W)
		SecTime1_entry = ttk.Entry(Groot, width=7, textvariable=self.SecTime1)
		SecTime1_entry.grid(column=2, row=3)

		# END TIME
		self.MinTime2 = IntVar()
		self.SecTime2 = IntVar()
		ttk.Label(Groot, text='End Time [min|sec]').grid(column=0, row=4)
		MinTime2_entry = ttk.Entry(Groot, width=7, textvariable=self.MinTime2)
		MinTime2_entry.grid(column=1, row=4, padx=1, sticky=tk.W)
		SecTime2_entry = ttk.Entry(Groot, width=7, textvariable=self.SecTime2)
		SecTime2_entry.grid(column=2, row=4)

		# BUTTONS
		ttk.Button(Groot, text="Input", command=self.inputter).grid(column=3, row=5, pady=4, sticky=tk.E)
		self.buttonDownFirst = ttk.Button(Groot, text="Download First")
		self.buttonDownFirst.grid(column=2, row=5)
		ttk.Button(Groot, text="Download All").grid(column=1, row=5, sticky=tk.W)

		# TEXT BOXES
		self.outT = Text(Groot, width=28, height=7, bd=1, padx=4, wrap=tk.WORD)
		self.clipT = Text(Groot, width=40, height=10, wrap=tk.WORD)
		self.outT.grid(column=0, row=6, columnspan=1, sticky=tk.W)
		self.clipT.grid(column=1, row=6, columnspan=4, sticky=tk.E)

		# READING CLIPS FROM FILE AND PRINTING
		try:
			printClips = json.load(open('clips.json', 'r'))
			for clip in printClips:
				self.clipT.insert(END, f'\nURL:{clip["URL"]}\nSTART:{clip["START"]}\nEND:{clip["END"]}\n')
		except:
			self.outT.insert(INSERT, f'({datetime.now().strftime("%H:%M:%S")}) NO CLIPS FOUND\n')

	def getOutT(self):
		return self.outT
	def getClipT(self):
		return self.clipT
	def getPathT(self):
		return self.pathT
	def getPathFF(self):
		return self.pathFF

	def inputter(self):
		time1 = self.MinTime1.get()*60+self.SecTime1.get()
		time2 = self.MinTime2.get()*60+self.SecTime2.get()
		try:
			json.dump(json.load(open('clips.json', 'r')) + [{'URL': self.url.get(), 'START': time1, 'END': time2}], open('clips.json', 'w'), indent=3)
		except:
			json.dump([], open('clips.json', 'w'))
			json.dump(json.load(open('clips.json', 'r')) + [{'URL': self.url.get(), 'START': time1, 'END': time2}], open('clips.json', 'w'), indent=3)
		self.clipT.insert(END, f'\nURL: {self.url.get()}\nSTART: {time1}\nEND: {time2}\n')
		self.outT.insert(INSERT, f'({datetime.now().strftime("%H:%M:%S")}) WRITE DONE\n')

	def setPath(self, tBox):
		path = fd.askdirectory(initialdir="Downloads", mustexist=False)
		tBox.delete('1.0', '3.0')
		tBox.insert('1.0', path+'/')

	def setButtonFunctions(self, commandVar):
		self.buttonDownFirst.config(command=commandVar)