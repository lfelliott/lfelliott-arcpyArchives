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
fcs = arcpy.ListFeatureClasses("*", "polygon")
fcs = ["p5_north_working", "p5_west_working", "p5_south_working"]
# fcs = ["test"]
# fcs = ["p5_west_working", "p5_south_working"]

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
		southstrs.append(ripstrstr)
	northstrs = ripstrs

for fc in fcs:
	print "\nProcessing: " + fc
	outf.writelines("\nProcessing: "+fc)
	layername = "l_"+fc
	DM.MakeFeatureLayer(fc, layername)
	processstart = time()
	if (fc == "p5_north_working"):
		selectstrs = northstrs
	if (fc == "p5_west_working"):
		selectstrs = weststrs
	if (fc == "p5_south_working"):
		selectstrs = southstrs
	for selectstr in selectstrs:
		print "Applying selection: " + selectstr
		DM.SelectLayerByAttribute(layername, "NEW_SELECTION", selectstr)
		DM.CalculateField(layername, "VegNum", selectdict[selectstr], "VB", "")
		print "Time to apply riparian models = " + elapsed_time(processstart)
	outf.writelines("Completed applying riparian models to " + fc + ": " + elapsed_time(processstart) + "\n")

print "process time = " + elapsed_time(processstart)
outf.writelines("\nCompleted select and calculate field. " + elapsed_time(processstart) + "\n")
processstart = time()

	
print "Finished - Elapsed Time = " + elapsed_time(starttime)
outf.writelines("\nFinished. " + elapsed_time(starttime) + "\n\n")
outf.close()
