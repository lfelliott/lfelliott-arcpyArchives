import os
currentdir = os.getcwd()
print currentdir
filelist = []
for filename in os.listdir(currentdir):
	if (filename[-3:] == "pyc"):
		filelist.append(filename)
for fname in filelist:
	print fname
	