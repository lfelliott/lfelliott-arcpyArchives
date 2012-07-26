import arcpy
from arcpy import management as DM
from time import time
from string import zfill
from datetime import date
arcpy.env.workspace = "C:/WorkSpace/Phase5"
outf = open("c:/workspace/phase5/modellog.txt", "a")
outf.writelines("\n" + str(date.today()) + " --Test--\n")


def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

# Apply models from key in separate dbf for each landcover
suffixes = ["01","03","05","07","09","11","13","15","19","21","23","25","27","31"]
covers = [1,3,5,7,9,11,13,15,19,21,23,25,27,31]
starttime = time()


objects_gdb = "p5_objects_working.gdb/"
objects
layername = "central_layer"
blegobjs = "Subsets.gdb/bleg"
bleg = "bleg_layer"
leader = "QKEY%s.dbf"
DM.MakeFeatureLayer(objects, layername)
DM.MakeFeatureLayer(blegobjs, bleg)
processstart = time()
for i in range(len(suffixes)):
	qname = leader % suffixes[i]
	qsystem = "[QKEY%s.SYSTEM]" % suffixes[i]
	qrmjoin = "QKEY%s" % suffixes[i]
	landcover = "\"central_objects.lulc\" = %s" % covers[i]
	print qname, qsystem, qrmjoin, landcover
	print "joining....."
	DM.AddJoin(layername, "Ecogroup", qname, "ECOGROUP", "KEEP_ALL")
	print "selecting....."
	DM.SelectLayerByAttribute(layername, "NEW_SELECTION", landcover)
	print "calculating....."
	DM.CalculateField(layername, "central_objects.VegNum", qsystem, "VB", "")
	print "removing join....."
	DM.RemoveJoin(layername, qrmjoin)
	print "clearing selection....."
	DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying models. " + elapsed_time(processstart) + "\n")
processstart = time()

# Update VegName using legend in exported dbf table	
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
legend = "P4LEG.DBF"
print "adding VegName......"
DM.AddJoin(layername, "VegNum", legend, "VEGNUM", "KEEP_ALL")
DM.CalculateField(layername, "central_objects.VegName", "[P4LEG.VEGNAME]", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
DM.RemoveJoin(layername, "P4LEG")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed updating VegName. " + elapsed_time(processstart) + "\n")
processstart = time()

# Apply riparian models to NHD24 buffers
# Selecting objects within Edwards Plateau Basin basin within riparian buffer or having riparian or ramadero soils
EP_RIP = "EP_RIP.DBF"
print "applying EP Riparian...."
DM.AddJoin(layername, "lulc", EP_RIP, "COVERTYPE", "KEEP_ALL")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"central_objects.Basin\" = 'Edwards Plateau' and ( \"central_objects.riparian24\" = 1  or \"central_objects.Vegname\" like '%Riparian%' or \"central_objects.Vegname\" = 'Ramadero') and \"central_objects.Ecogroup\" not like '%Bottomland%'")
DM.CalculateField(layername, "central_objects.VegNum", "[EP_RIP.SYSTEM]", "VB", "")
DM.RemoveJoin(layername, "EP_RIP")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying EP Riparian. " + elapsed_time(processstart) + "\n")
processstart = time()

# Selecting objects within Tamaulipan basin within riparian buffer or having riparian or ramadero soils
TAM_RIP = "TAM_RIP.DBF"
print "applying TAM Riparian...."
DM.AddJoin(layername, "lulc", TAM_RIP, "COVERTYPE", "KEEP_ALL")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"central_objects.Basin\" = 'Tamaulipan' and ( \"central_objects.riparian24\" = 1  or \"central_objects.Vegname\" like '%Riparian%' or \"central_objects.Vegname\" = 'Ramadero')and \"central_objects.Ecogroup\" not like '%Bottomland%'")
DM.CalculateField(layername, "central_objects.VegNum", "[TAM_RIP.SYSTEM]", "VB", "")
DM.RemoveJoin(layername, "TAM_RIP")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying Tamaulipan riparian. " + elapsed_time(processstart) + "\n")
processstart = time()

# Remove juniper from outside range of juniper.
print "moving juniper woodland to live oak woodland  outside of range....."
NonJuniper = "Subsets.gdb/Juniper"
# Floodplain 1001 > 1002 = Juniper to Live oak
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 1001 or \"VegNum\" = 1003")
DM.SelectLayerByLocation(layername, "INTERSECT", NonJuniper, "", "REMOVE_FROM_SELECTION")
DM.CalculateField(layername, "VegNum", "1002", "VB", "")
# Floodplain Juniper shrub (1005) to Deciduous Shrub (1006)
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 1005")
DM.SelectLayerByLocation(layername, "INTERSECT", NonJuniper, "", "REMOVE_FROM_SELECTION")
DM.CalculateField(layername, "VegNum", "1006", "VB", "")
# Riparian Juniper Woodland (1401) > Live Oak (1402)
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 1401 or \"VegNum\" = 1403")
DM.SelectLayerByLocation(layername, "INTERSECT", NonJuniper, "", "REMOVE_FROM_SELECTION")
DM.CalculateField(layername, "VegNum", "1402", "VB", "")
# Riparian Juniper shrub (1405) to Deciduous Shrub (1406)
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 1405")
DM.SelectLayerByLocation(layername, "INTERSECT", NonJuniper, "", "REMOVE_FROM_SELECTION")
DM.CalculateField(layername, "VegNum", "1406", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed removing out of range juniper. " + elapsed_time(processstart) + "\n")
processstart = time()

# Add Sandylands to specific objects
print "add Sandylands"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"OBJECTID\" = 304264 or \"OBJECTID\" = 304272 or \"OBJECTID\" = 304281 or \"OBJECTID\" = 304284 or \"OBJECTID\" = 323092 or \"OBJECTID\" = 323094 or \"OBJECTID\" = 323095")
DM.CalculateField(layername, "VegNum", "706", 'VB", "")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"OBJECTID\" = 304286")
DM.CalculateField(layername, "VegNum", "707", "VB", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed addition of Sandylands. " + elapsed_time(processstart) + "\n")
processstart = time()

# Add Live Oak types to sandy and floodplain areas of the South Texas Plains
print "add live oak types to sandy/floodplain of South Texas"
DM.SelectLayerByAttribute(bleg, "NEW_SELECTION", "\"Type\" = 'Live Oak'")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 7103 and \"lulc\" = 3")
DM.SelectLayerByLocation(layername, "INTERSECT", bleg, "", "SUBSET_SELECTION")
DM.CalculateField(layername, "VegNum", "7102", "VB", "")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 7402 and \"lulc\" = 3")
DM.SelectLayerByLocation(layername, "INTERSECT", bleg, "", "SUBSET_SELECTION")
DM.CalculateField(layername, "VegNum", "7412", "VB", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed live oak corrections. " + elapsed_time(processstart) + "\n")
processstart = time()

# Next 2 blocks added 8/3/2011
print "adding cliffs.."
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "(\"VegNum\" = 1101 or \"VegNum\" = 1102 or \"VegNum\" = 1103 or \"VegNum\" = 1104 or \"VegNum\" = 1205 or \"VegNum\" = 1206) and \"cliff\" = 1")
DM.CalculateField(layername, "VegNum", "806", "VB", "")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "(\"VegNum\" = 1107 or \"VegNum\" = 9000) and \"cliff\" = 1")
DM.CalculateField(layername, "VegNum", "807", "VB", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed adding cliffs. " + elapsed_time(processstart) + "\n")
processstart = time()

# Correct slope types
print "correcting slope types...."
slopes = "SLPXWALK.dbf"
DM.AddJoin(layername, "VegNum", slopes, "STANDARD", "KEEP_ALL")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"SLPXWALK.SLOPE\" is not null AND \"central_objects.slope20\" =1 AND \"central_objects.cliff\" = 0")
DM.CalculateField(layername, "central_objects.VegNum", "[SLPXWALK.SLOPE]", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
DM.RemoveJoin(layername, "SLPXWALK")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying slopes. " + elapsed_time(processstart) + "\n")
processstart = time()
# previous 2 blocks added 8/3/2011

# Update VegName using legend in exported dbf table	
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "adding VegName......"
DM.AddJoin(layername, "VegNum", legend, "VEGNUM", "KEEP_ALL")
DM.CalculateField(layername, "central_objects.VegName", "[P4LEG.VEGNAME]", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
DM.RemoveJoin(layername, "P4LEG")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed updating VegName. " + elapsed_time(processstart) + "\n")
processstart = time()


# Dissolve on VegNum/VegName to north_dslv
print "dissolving on Vegnum/VegName..."
dslv = "p4_objects_working.gdb/central_dslv"
try:
	DM.Dissolve(objects, dslv, "VegNum;VegName", "", "MULTI_PART", "DISSOLVE_LINES")
	print "process time = " + elapsed_time(processstart)
	outf.writelines("Completed dissolve. " + elapsed_time(processstart) + "\n")
	processstart = time()
except:
	outf.writelines("Aborted dissolve. " + elapsed_time(processstart) + "\n")
	print "Exited - Elapsed Time = " + elapsed_time(starttime)
	exit()

# Repair geometry
print "Starting repair geometry......"
try:
	DM.RepairGeometry(dslv, "DELETE_NULL")
	print "Repair geometry process time = " + elapsed_time(processstart)
	outf.writelines("Completed repair geometry. " + elapsed_time(processstart) + "\n")
except:
	outf.writelines("Aborted repair geometry. " + elapsed_time(processstart) + "\n")
	print "Exited - Elapsed Time = " + elapsed_time(starttime)
	exit()


print "Finished - Elapsed Time = " + elapsed_time(starttime)
outf.writelines("\nFinished. " + elapsed_time(starttime) + "\n\n")
outf.close()
