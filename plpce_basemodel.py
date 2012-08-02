import arcpy
import os
import csv
from arcpy import management as DM
from time import time
from string import zfill
from datetime import date
arcpy.env.workspace = "D:\\Projects\\Oklahoma\\GIS\\LPCE_Objects_07_26_12.gdb"
outf = open("D:\\Projects\\Oklahoma\\GIS\\modellog.txt", "a")
outf.writelines("\n" + str(date.today()) + " --Phase LPCE --\n")


def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

starttime = time()
processstart = time()

# Apply models from key in separate dbf for each landcover
suffixes = ["01","02","03","06","10"]
covers = [1,2,3,6,10]
leader = "QKEY%s.dbf"

fcs = arcpy.ListFeatureClasses("*", "polygon")
fcs = ["p5_north_working", "p5_west_working", "p5_south_working"]
# fcs = ["test"]
# fcs = ["p5_west_working", "p5_south_working"]

fc = "LPCE_Objects"
processstart = time()
print "\nProcessing: "+fc
layername = "l_"+fc
DM.MakeFeatureLayer(fc, layername)
# 	Apply simple models
for i in range(len(suffixes)):
	qname = leader % suffixes[i]
	qsystem = "[QKEY%s.VEGTYPE]" % suffixes[i]
	qrmjoin = "QKEY%s" % suffixes[i]
	landcover = "\"%s.lulc\" = %s" % (fc, covers[i])
	print qname, qsystem, qrmjoin, landcover
	print "joining....."
	DM.AddJoin(layername, "Ecogroup", qname, "ECOGROUP", "KEEP_ALL")
	print "selecting....."
	DM.SelectLayerByAttribute(layername, "NEW_SELECTION", landcover)
	print "calculating....."
	calcfield = "%s.VegNum" % fc
	DM.CalculateField(layername, calcfield, qsystem, "VB", "")
	print "removing join....."
	DM.RemoveJoin(layername, qrmjoin)
	print "clearing selection....."
	DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("\nCompleted applying simple models to " + fc + ": " + elapsed_time(processstart) + "\n")
	

print "Finished - Elapsed Time = " + elapsed_time(starttime)
outf.writelines("\nFinished. " + elapsed_time(starttime) + "\n\n")
outf.close()
