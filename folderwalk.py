import os
import re
import arcpy

str2 = r'\US_100ESP'
startpath = 'd:\\perl\\Python'

i=1
for dirname, dirnames, filenames in os.walk(startpath):
	for subdirname in dirnames:
		workingpath = os.path.join(dirname, subdirname)
		if (workingpath[-10:] == str2):
			commonname = workingpath+"\\us_100esp"
			newname = commonname+"_"+str(i)
			i = i + 1
			print commonname+" TO "+newname
			arcpy.Rename_management(commonname, newname)
