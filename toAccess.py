import arcpy
import os
import csv
from arcpy import management as DM
from time import time
from string import zfill
from datetime import date
arcpy.env.workspace = "C:/WorkSpace/Phase5/Objects/p5_working.gdb"
outf = open("c:/workspace/phase5/Objects/modellog.txt", "a")
outf.writelines("\n" + str(date.today()) + " -- Export Phase 5 to dbfs --\n")


def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

starttime = time()
processstart = time()

outpath = "C:\\WorkSpace\\Phase5\\Objects"
fc = "p5_north_working"
outdbf = "north.dbf"

layername = "l_"+fc
DM.MakeFeatureLayer(fc, layername)
arcpy.TableToTable_conversion(fc, outpath, outdbf)
print "\nFinished exporting " + fc + " to " + outdbf + " in " + elapsed_time(processstart)
processstart = time()

fc = "p5_west_working"
outdbf = "west.dbf"

layername = "l_"+fc
DM.MakeFeatureLayer(fc, layername)
arcpy.TableToTable_conversion(fc, outpath, outdbf)
print "\nFinished exporting " + fc + " to " + outdbf + " in " + elapsed_time(processstart)
processstart = time()

fc = "p5_south_working"
outdbf = "south.dbf"

layername = "l_"+fc
DM.MakeFeatureLayer(fc, layername)
arcpy.TableToTable_conversion(fc, outpath, outdbf)
print "\nFinished exporting " + fc + " to " + outdbf + " in " + elapsed_time(processstart)
processstart = time()


print "Finished - Elapsed Time = " + elapsed_time(starttime)
outf.writelines("\nFinished. " + elapsed_time(starttime) + "\n\n")
outf.close()