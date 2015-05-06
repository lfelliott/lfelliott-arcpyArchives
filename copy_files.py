import os
import shutil
infile = open('missing_files.txt', 'r')
while (1):
	line = infile.readline()[:-1]
	if not line: break
	shutil.copy(line, 'keep/%s' % line)