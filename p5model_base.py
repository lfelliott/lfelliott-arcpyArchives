import arcpy
import os
import csv
from arcpy import management as DM
from time import time
from string import zfill
from datetime import date
arcpy.env.workspace = "C:/WorkSpace/Phase5/Objects/p5_working.gdb"
outf = open("c:/workspace/phase5/Objects/modellog.txt", "a")
outf.writelines("\n" + str(date.today()) + " --Phase 5 --\n")


def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

starttime = time()
processstart = time()

# Apply models from key in separate dbf for each landcover
suffixes = ["01","03","05","07","09","11","15","19","21","23","25","27","31"]
covers = [1,3,5,7,9,11,15,19,21,23,25,27,31]
leader = "QKEY%s.dbf"

fcs = arcpy.ListFeatureClasses("*", "polygon")
fcs = ["p5_north_working", "p5_west_working", "p5_south_working"]
# fcs = ["test"]
# fcs = ["p5_west_working", "p5_south_working"]

# Build complex selection strings
rows = csv.reader(open('p5cmplx.csv', 'rb'), delimiter = ',', quotechar='"')
selectstrs = []
selectdict = {}
for row in rows:
	ecogrp = row[0]
	landcover = row[1]
	vegtype = row[2]
	gt_elev = row[3]
	lt_elev = row[4]
	gt_slope = row[5]
	lt_slope = row[6]
	gt_insol = row[7]
	lt_insol = row[8]
	selectstr = "\"EcoGroup\" = '%s' AND \"lulc\" = %s" % (ecogrp, landcover)
	if (gt_elev):
		selectstr = selectstr + " AND \"elev\" > " + gt_elev
	if (lt_elev):
		selectstr = selectstr + " AND \"elev\" <= " + lt_elev
	if (gt_slope):
		selectstr = selectstr + " AND \"slp\" > " + gt_slope
	if (lt_slope):
		selectstr = selectstr + " AND \"slp\" <= " + lt_slope
	if (gt_insol):
		selectstr = selectstr + " AND \"insol\" > " + gt_insol
	if (lt_insol):
		selectstr = selectstr + " AND \"insol\" <= " + lt_insol
	selectstrs.append(selectstr)
	selectdict[selectstr] = vegtype

# Build riparian selection strings	
riprows = csv.reader(open('riparian.csv', 'rb'), delimiter = ',', quotechar='"')
ripstrs = []
weststrs = []
southstrs = []
northstrs = []
ripdict = {}
for riprow in riprows:
	ripstr = ""
	floodpl = riprow[0]
	landcover = riprow[1]
	vegtype = riprow[2]
	gt_elev = riprow[3]
	lt_elev = riprow[4]
	ripstr = "\"floodpl\" = '%s' AND \"riparian24\" = 1 AND \"lulc\" = %s" % (floodpl, landcover)
	if (gt_elev):
		ripstr = ripstr + " AND \"elev\" > " + gt_elev
	if (lt_elev):
		ripstr = ripstr + " AND \"elev\" <= " + lt_elev
	ripdict[ripstr] = vegtype
	ripstrs.append(ripstr)
	if (floodpl == "CH"):
		weststrs.append(ripstr)
		southstrs.append(ripstr)
	if (floodpl == "SP"):
		southstrs.append(ripstr)
	northstrs = ripstrs
ripstrs = []

print "\nSetup took " + elapsed_time(processstart) + "\n"	

for fc in fcs:
	processstart = time()
	outf.writelines("\nProcessing: "+fc)
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
	
#	Apply complex models
	processstart = time()
	for selectstr in selectstrs:
		print "Applying selection: " + selectstr
		DM.SelectLayerByAttribute(layername, "NEW_SELECTION", selectstr)
		if (int(str(DM.GetCount(layername))) > 0):
			DM.CalculateField(layername, "VegNum", selectdict[selectstr], "VB", "")
		DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
		print "Time to apply complex models = " + elapsed_time(processstart)
	outf.writelines("Completed applying complex models to " + fc + ": " + elapsed_time(processstart) + "\n")

#	Apply riparian models
	processstart = time()
	if (fc == "p5_north_working"):
		ripstrs = northstrs
	if (fc == "p5_west_working"):
		ripstrs = weststrs
	if (fc == "p5_south_working"):
		ripstrs = southstrs
	for ripstr in ripstrs:
		print "\nApplying riparian selection: " + ripstr
		DM.SelectLayerByAttribute(layername, "NEW_SELECTION", ripstr)
		if (int(str(DM.GetCount(layername))) > 0):
			DM.CalculateField(layername, "VegNum", ripdict[ripstr], "VB", "")
	print "Time to apply riparian models = " + elapsed_time(processstart)
	outf.writelines("Completed applying riparian models to " + fc + ": " + elapsed_time(processstart) + "\n")

print "Finished - Elapsed Time = " + elapsed_time(starttime)
outf.writelines("\nFinished. " + elapsed_time(starttime) + "\n\n")
outf.close()
