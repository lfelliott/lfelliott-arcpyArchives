import arcpy
from arcpy import management as DM
arcpy.env.workspace = "c:/WorkSpace/Phase4"
from time import time
from string import zfill
from datetime import date

outf = open ("c:/workspace/phase4/modellog.txt", "a")
outf.writelines("\n" + str(date.today()) + " ---Merge all and dissolve---\n")
def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

# Local variables:
central_dslv = "p4_objects_working.gdb\\central_dslv"
north_dslv = "p4_objects_working.gdb\\north_dslv"
south_dslv = "p4_objects_working.gdb\\south_dslv"
p4merged = "p4_objects_working.gdb\\p4_merged"
p4veg = "p4_objects_working.gdb\\p4veg"
starttime = time()
processstart = time()

#Process: Repair geometry north
#print "Starting repair geometry north......"
#DM.RepairGeometry(north_dslv, "DELETE_NULL")
#print "Repair geometry north process time = " + elapsed_time(processstart)
#outf.writelines("Completed repair geometry north. " + elapsed_time(processstart) + "\n")
#processstart = time()

#Process: Repair geometry central
#print "Starting repair geometry......"
#DM.RepairGeometry(central_dslv, "DELETE_NULL")
#print "Repair geometry central process time = " + elapsed_time(processstart)
#outf.writelines("Completed repair geometry central. " + elapsed_time(processstart) + "\n")
#processstart = time()

#Process: Repair geometry south
print "Starting repair geometry south......"
DM.RepairGeometry(south_dslv, "DELETE_NULL")
print "Repair geometry south process time = " + elapsed_time(processstart)
outf.writelines("Completed repair geometry south. " + elapsed_time(processstart) + "\n")
processstart = time()

# Process: Merge
DM.Merge("p4_objects_working.gdb\\central_dslv;p4_objects_working.gdb\\north_dslv;p4_objects_working.gdb\\south_dslv", p4merged, "VegNum \"VegNum\" true true false 4 Long 0 0 ,First,#,p4_objects_working.gdb\\central_dslv,VegNum,-1,-1,p4_objects_working.gdb\\north_dslv,VegNum,-1,-1,p4_objects_working.gdb\\south_dslv,VegNum,-1,-1;VegName \"VegName\" true true false 100 Text 0 0 ,First,#,p4_objects_working.gdb\\central_dslv,VegName,-1,-1,p4_objects_working.gdb\\north_dslv,VegName,-1,-1,p4_objects_working.gdb\\south_dslv,VegName,-1,-1;Shape_Length \"Shape_Length\" false true true 8 Double 0 0 ,First,#,p4_objects_working.gdb\\central_dslv,Shape_Length,-1,-1,p4_objects_working.gdb\\north_dslv,Shape_Length,-1,-1,p4_objects_working.gdb\\south_dslv,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0 ,First,#,p4_objects_working.gdb\\central_dslv,Shape_Area,-1,-1,p4_objects_working.gdb\\north_dslv,Shape_Area,-1,-1,p4_objects_working.gdb\\south_dslv,Shape_Area,-1,-1")
print "Merge process time = " + elapsed_time(processstart)
outf.writelines("Completed merge. " + elapsed_time(processstart) + "\n")
processstart = time()

#Process: Repair geometry
print "Starting repair geometry merged......"
DM.RepairGeometry(p4merged, "DELETE_NULL")
print "Repair geometry process time = " + elapsed_time(processstart)
outf.writelines("Completed repair geometry. " + elapsed_time(processstart) + "\n")
processstart = time()

# Process: Dissolve
#print "Starting dissolve, single part....."
#DM.Dissolve(p4merged, p4veg, "VegNum;VegName", "", "SINGLE_PART", "DISSOLVE_LINES")
#print "Merge process time = " + elapsed_time(processstart)
#outf.writelines("Completed dissolve, single part. " + elapsed_time(processstart) + "\n")
#processstart = time()

print "Starting dissolve, multi part....."
p4veg_mp = "p4_objects_working.gdb\\p4veg_mp"
arcpy.Dissolve_management(p4merged, p4veg2, "VegNum;VegName", "", "MULTI_PART", "DISSOLVE_LINES")
outf.writelines("Completed dissolve, multi part. " + elapsed_time(processstart) + "\n")

print "Finished - Elapsed Time = " + elapsed_time(starttime)
outf.writelines("\nFinished. " + elapsed_time(starttime) + "\n\n")
outf.close()
