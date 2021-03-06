import arcpy
from arcpy import management as DM
from time import time
from string import zfill
from datetime import date
arcpy.env.workspace = "C:/Documents and Settings/lfelliott/My Documents/ArcGIS"

outf = open ("C:/Documents and Settings/lfelliott/My Documents/ArcGIS/modellog.txt", "a")
outf.writelines("\n" + str(date.today()) + " ---North dissolve---\n")
def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)


starttime = time()
objects = "p4_objects_working.gdb/north_objects"
dslv = "p4_objects_working.gdb/north_dslv"
processstart = time()

# Dissolve on VegNum/VegName to south_dslv
print "dissolving on Vegnum/VegName..."
try:
	DM.Dissolve(objects, dslv, "VegNum;VegName", "", "MULTI_PART", "DISSOLVE_LINES")
	outf.writelines("Completed dissolve. " + elapsed_time(processstart) + "\n")
	processstart = time()
except:
	outf.writelines("Aborted dissolve. " + elapsed_time(processstart) + "\n")
	print "Exited - Elapsed Time = " + elapsed_time(starttime)
	exit()

# Repair geometry
#print "Starting repair geometry......"
#try:
#	DM.RepairGeometry(dslv, "DELETE_NULL")
#	print "Repair geometry process time = " + elapsed_time(processstart)
#	outf.writelines("Completed repair geometry. " + elapsed_time(processstart) + "\n")
#except:
#	outf.writelines("Aborted Repair Geometry. " + elapsed_time(processstart) + "\n")
#	print "Exited - Elapsed Time = " + elapsed_time(starttime)
#	exit()

outf.writelines("Finised dissolve " + elapsed_time(starttime) + "\n")
print "Finished - Elapsed Time = " + elapsed_time(starttime)
outf.close()
