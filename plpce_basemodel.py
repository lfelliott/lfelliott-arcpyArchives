import arcpy
import os
import csv
from arcpy import management as DM
from time import time
from string import zfill
from datetime import date
arcpy.env.workspace = "D:\\Projects\\Oklahoma\\GIS\\LPCE_Working.gdb"
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

fc = "LPCE_working"

processstart = time()
print "\nProcessing: "+fc
layername = "l_"+fc
DM.MakeFeatureLayer(fc, layername)
print "change crop to grass outside of clu"
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION")
DM.CalculateField(layername, "lulc", "[MAJORITY]", "VB", "")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"MAJORITY\" = 5 AND \"CLUCLSCD\" <> 2")
DM.CalculateField(layername, "lulc", 1, "VB", "")

# 	Apply simple models
calcfield = "%s.VegNum" % fc
for i in range(len(suffixes)):
	qname = leader % suffixes[i]
	qsystem = "[QKEY%s.VEGNUM]" % suffixes[i]
	qrmjoin = "QKEY%s" % suffixes[i]
	qfullname = "D:\\Projects\\Oklahoma\\GIS\\%s.dbf" % qrmjoin
	landcover = "\"%s.lulc\" = %s" % (fc, covers[i])
	selectstr = "\"%s.lulc\" = %s" % (fc, covers[i])
	print qname, qsystem, qrmjoin, landcover
	print "joining....."
	DM.AddJoin(layername, "Ecoclassid", qfullname, "ECOCLASSID", "KEEP_COMMON")
	print "selecting....."
	DM.SelectLayerByAttribute(layername, "NEW_SELECTION", selectstr)
	print "calculating....."
	DM.CalculateField(layername, calcfield, qsystem, "VB", "")
	print "removing join....."
	DM.RemoveJoin(layername, qrmjoin)
	print "clearing selection....."
	DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("\nCompleted applying simple models to " + fc + ": " + elapsed_time(processstart) + "\n")

print "processing water"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"lulc\" = 4")
DM.CalculateField(layername, "VegNum", 9600, "VB", "")

print "processing water in playa"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"lulc\" = 4 AND (\"Ecoclassid\" = 'R077AY005TX' OR \"Ecoclassid\" = 'R078BY078TX') AND \"CLUCLSCD\" <> 2")
DM.CalculateField(layername, "VegNum", 6900, "VB", "")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"lulc\" = 4 AND (\"Ecoclassid\" = 'R077AY005TX' OR \"Ecoclassid\" = 'R078BY078TX') AND \"CLUCLSCD\" = 2")
DM.CalculateField(layername, "VegNum", 9307, "VB", "")

print "processing crops"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"lulc\" = 5")
DM.CalculateField(layername, "VegNum", 9307, "VB", "")

print "processing grass to crp in clus"
selectstrclu = "(\"lulc\" = 1 or \"lulc\" = 2 or \"lulc\" = 3) and \"CLUCLSCD\" = 2"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", selectstrclu)
DM.CalculateField(layername, "VegNum", 9327, "VB", "")
print "processing barren in clu to crop"
selectstrclu = "\"lulc\" = 6 and \"CLUCLSCD\" = 2"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", selectstrclu)
DM.CalculateField(layername, "VegNum", 9307, "VB", "")

print "processing urban low"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"lulc\" = 8")
DM.CalculateField(layername, "VegNum", 9411, "VB", "")

print "processing urban high"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"lulc\" = 9")
DM.CalculateField(layername, "VegNum", 9410, "VB", "")

print "process riparian"
DM.AddJoin(layername, "lulc", "D:\\Projects\\Oklahoma\\GIS\\RIP.dbf", "COVERTYPE", "KEEP_COMMON")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "(\"lulc\" = 1 OR \"lulc\" = 2 or \"lulc\" = 3 or \"lulc\" =6 or \"lulc\" = 10 or \"lulc\" = 11) and \"Riparian\" = 1 and \"VegNum\" <> 9327")
DM.CalculateField(layername, calcfield, "[RIP.SYSTEM]", "VB", "")

print "process slope"
selectslpbase = "(\"Ecoclassid\" = 'R078BY081TX' OR \"Ecoclassid\" = 'R078BY088TXN' or \"Ecoclassid\" = 'R078BY090TX' or \"Ecoclassid\" = 'R078BY092TX' or \"Ecoclassid\" = 'R078CY114TX' OR \"Ecoclassid\" = 'R078CY112TX') and \"Slope\" = 20 AND "
selectslp = "%s\"lulc\" = 2" % selectslpbase
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", selectslp)
DM.CalculateField(layername, calcfield, 2106, "VB", "")
selectslp = "%s\"lulc\" = 3" % selectslpbase
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", selectslp)
DM.CalculateField(layername, calcfield, 2105, "VB", "")	

print "Finished - Elapsed Time = " + elapsed_time(starttime)
outf.writelines("\nFinished. " + elapsed_time(starttime) + "\n\n")
outf.close()
