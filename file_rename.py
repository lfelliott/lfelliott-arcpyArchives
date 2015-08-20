import os

files = []
for (dirpath, dirnames, filenames) in os.walk("."):
	files.extend(filenames)
	break
for file in files:
	if "las" in file: 
		newname = file.replace(".las-monroe", "-monroe")
#		print newname
		os.rename(line, newline)