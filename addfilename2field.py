# addfilename2field.py
# 27 Jun 2011
# L. Elliott
#
# Python script to add a field and fill the field with the filename of the shapefile. A list of shapefiles
# is provided in a file "dir.txt" and the shapefiles, this python script, and the "dir.txt" file are within one
# folder. This folder is identified in arcpy.env.workspace below.
#
import os
import arcpy
from arcpy import management as DM

# Change the following lines to reflect differences in your setup
# arcpy.env.workspace = folder the dir.txt, shapefiles, and this script are found in. Notice that the
#                       slash is a forward slash.
# fldname = the name of the field you want to add and fill, in this case "filename"
# dir_file = the name of the file housing the list of shapefiles, in this case "dir.txt"

currentdir = os.getcwd()
arcpy.env.workspace = currentdir
fldname = "filename"


filelist = []
for filename in os.listdir(currentdir):
	if (filename[-3:] == "shp"):
		filelist.append(filename)
	
for fname in filelist:
	print "Doing %s....\n" % fname
	fnamestr = "\"%s\"" % fname
	try:
		DM.AddField(fname, fldname, "TEXT", "", "", "150", "", "NON_NULLABLE", "NON_REQUIRED", "")
	except:
		print "Error in adding field to %s\n" % fname
		continue
	try:	
		DM.CalculateField(fname, fldname, fnamestr, "VB", "")
	except:
		print "Error adding filename to shapefile %s\n" % fnames[i]
		continue
		
