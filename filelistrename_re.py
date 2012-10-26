import os
import re
currentdir = os.getcwd()
searchstr = re.compile(r'mapunit_(\d{1,2}).dbf$')
filelist = []
for filename in os.listdir(currentdir):
	m1 = searchstr.match(filename)
	if m1:
		p1 = m1.group(1)
		newname = "mu" + str(p1) + ".dbf"
		print filename + " > " + newname
		os.rename(filename, newname)
	