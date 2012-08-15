import arcpy
import os
import csv
from arcpy import management as DM
from time import time
from string import zfill
from datetime import date
arcpy.env.workspace = "D:\\Projects\\Oklahoma\\GIS\\OK_Objects_MR_7_25_12.gdb"
outf = open("D:\\Projects\\Oklahoma\\GIS\\modellog.txt", "a")
outf.writelines("\n" + str(date.today()) + " --Phase LPCE --\n")


def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)


def applyrule(layername, rulestr, ruletype):
	DM.SelectLayerByAttribute(layername, "NEW_SELECTION", rulestr)
	DM.CalculateField(layername, "VegNum", ruletype, "VB", "")
fc = "OK_Objects_All_7_25_12"
lname = "l_OK_Working_dslv"
DM.MakeFeatureLayer(fc, lname)
starttime = time()
processstart = time()
print "process slopes"
applyrule(lname, "(\"ecoclassid\" = 'R070AY005OK' or \"ecoclassid\" = 'R070AY039OK') and \"Slope\" = 20 and (\"MAJORITY\"  = 11 or \"MAJORITY\" = 4 or \"MAJORITY\" = 7)", 12705)
applyrule(lname, "(\"ecoclassid\" = 'R070AY005OK' or \"ecoclassid\" = 'R070AY039OK' or \"ecoclassid\" = 'R070AY054OK' or \"ecoclassid\" = 'R070AY099OK') and \"Slope\" = 20 and \"MAJORITY\" = 2", 12706)
applyrule(lname, "\"ecoclassid\" = 'R070AY054OK' and \"Slope\" = 20 and \"MAJORITY\" = 4", 12705)
applyrule(lname, "\"ecoclassid\" = 'R070AY099OK' and \"Slope\" = 20 and \"MAJORITY\" = 7", 12705)
applyrule(lname, "(\"ecoclassid\" = 'R077AY013TX' or \"ecoclassid\" = 'R077EY068TX') and \"Slope\" = 20 and \"MAJORITY\"  = 6", 2100)
applyrule(lname, "\"ecoclassid\" = 'R077EY068TX' and \"Slope\" = 20 and (\"MAJORITY\"  = 2 or \"MAJORITY\" = 4)", 2106)

print "process water"
applyrule(lname, "\"MAJORITY\" = 3", 9600)

print "process crops"
applyrule(lname, "\"MAJORITY\" = 5", 9307)
applyrule(lname, "\"MAJORITY\" = 6 and \"CLUCD\" = 2", 9307

print "process urban high"
applyrule(lname, "\"MAJORITY\" = 8", 9410)

print "process urban low"
applyrule(lname, "\"MAJORITY\" = 9", 9411)

print "process crp"
applyrule(lname, "(\"MAJORITY\" = 1 or \"MAJORITY\" = 2 or \"MAJORITY\" = 4) and \"CLUCD\" = 2", 9327)

print "process riparian"
applyrule(lname, "\"riparian\" = 1 and (\"MAJORITY\" = 2 or \"MAJORITY\" = 4)", 2706)
applyrule(lname, "\"riparian\" = 1 and (\"MAJORITY\" = 10 or \"MAJORITY\" = 11)", 2704)
applyrule(lname, "\"riparian\" = 1 and \"MAJORITY\" = 7", 3808)