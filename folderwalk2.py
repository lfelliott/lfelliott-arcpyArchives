import os
import re
import arcpy
import string

startpath = 'I:\\Landfire'
searchpath = re.compile(r'\\[USAKHI]{2}_100[ESPB]{3}$')
if not os.path.exists(startpath+"\\output"):
	os.makedirs(startpath+"\\output")
i=1
for dirname, dirnames, filenames in os.walk(startpath):
	for subdirname in dirnames:
		workingpath = os.path.join(dirname, subdirname)
		p1 = searchpath.search(workingpath)
		if p1:
			m1 = p1.group()
			commonname = workingpath+m1.lower()
			newname = startpath+"\\output\\"+m1.lower()+"_"+str(i)
			i = i + 1
			print commonname + " TO " + newname
			arcpy.Copy_management(commonname, newname)
