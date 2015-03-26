import os
currentdir = os.getcwd()
outfile = open('rename_list.csv', 'a')
print currentdir
filelist = []
for filename in os.listdir(currentdir):
	if (filename[-3:].upper() == "JPG"):
		filelist.append(filename)
outfile.write("oldname, newname\n")
for fname in filelist:
	newname = fname.replace('May 1', 'May1')
	newname = newname.replace(', 2', '_2')
	newname = newname.replace(' ', '_')
	os.rename(fname, newname)	
	outfile.write("\"%s\",%s\n" % (fname, newname))
	