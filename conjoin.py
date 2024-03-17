import os
import subprocess
'''
linenum = 1
charnum = 1
path = 'E:/FUNI/program/index'
with open('index.py', 'r') as f:
	lines = f.readlines()
	for line in lines:
		for char in line:
			file = open(f'{path}/{linenum}_{charnum}.txt', 'w')
			file.write(char)
			file.close()
			charnum += 1
		charnum = 1
		linenum += 1
'''
lines = []
tString = ''
linenum = 1
charnum = 0
while linenum > 0:
	try:
		charnum += 1
		with open(f'E:/FUNI/program/index/{linenum}_{charnum}.txt', 'r') as f:
			tString += f.read(1)
			print(tString)
	except:
		charnum = 0
		linenum += 1
		lines.append(tString)
		tString = ''
		try:
			charnum += 1
			with open(f'E:/FUNI/program/index/{linenum}_{charnum}.txt', 'r') as f:
				tString += f.read(1)
				print(tString)
		except:
			linenum = -1
			print("error")
print(lines)
separator = "\n"
exec(separator.join(lines))