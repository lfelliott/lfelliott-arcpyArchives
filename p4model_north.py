import arcpy
from arcpy import management as DM
from time import time
from string import zfill
arcpy.env.workspace = "C:/WorkSpace/Phase4"
from datetime import date


def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

# Apply models from key in separate dbf for each landcover
suffixes = ["01","03","05","07","09","11","13","15","19","21","23","25","27","31"]
covers = [1,3,5,7,9,11,13,15,19,21,23,25,27,31]
starttime = time()
objects = "p4_objects_working.gdb/north_objects"
soilobjs = "p4_soils_working.gdb/p4soils_working"
layername = "north_layer"
slayername = "soils"
leader = "QKEY%s.dbf"
outf = open("c:/workspace/phase4/modellog.txt", "a")
outf.writelines("\n" + str(date.today()) + " --North--\n")
DM.MakeFeatureLayer(objects, layername)
DM.MakeFeatureLayer(soilobjs, slayername)
processstart = time()
for i in range(len(suffixes)):
	qname = leader % suffixes[i]
	qsystem = "[QKEY%s.SYSTEM]" % suffixes[i]
	qrmjoin = "QKEY%s" % suffixes[i]
	landcover = "\"north_objects.lulc\" = %s" % covers[i]
	print qname, qsystem, qrmjoin, landcover
	print "joining....."
	DM.AddJoin(layername, "Ecogroup", qname, "ECOGROUP", "KEEP_ALL")
	print "selecting....."
	DM.SelectLayerByAttribute(layername, "NEW_SELECTION", landcover)
	print "calculating....."
	DM.CalculateField(layername, "north_objects.VegNum", qsystem, "VB", "")
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
DM.CalculateField(layername, "north_objects.VegName", "[P4LEG.VEGNAME]", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
DM.RemoveJoin(layername, "P4LEG")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed updating VegName. " + elapsed_time(processstart) + "\n")
processstart = time()

# Apply riparian models to NHD24 buffers
# Selecting objects within EP basin within riparian buffer or having riparian or ramadero soils
EP_RIP = "EP_RIP.DBF"
print "applying EP Riparian...."
DM.AddJoin(layername, "lulc", EP_RIP, "COVERTYPE", "KEEP_ALL")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"north_objects.Basin\" = 'Edwards Plateau' and ( \"north_objects.riparian24\" = 1  or \"north_objects.Vegname\" like '%Riparian%' or \"north_objects.Vegname\" = 'Ramadero') and \"north_objects.EcoGroup\" not like '%Bottomland%'")
DM.CalculateField(layername, "north_objects.VegNum", "[EP_RIP.SYSTEM]", "VB", "")
DM.RemoveJoin(layername, "EP_RIP")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying Edwards Plateau riparian. " + elapsed_time(processstart) + "\n")
processstart = time()

# Selecting objects within Chihuahuan basin, excluding riparian buffer, or having riparian or ramadero soils
CH_RIP = "CH_RIP.DBF"
print "applying CH Riparian...."
DM.AddJoin(layername, "lulc", CH_RIP, "COVERTYPE", "KEEP_ALL")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"north_objects.Basin\" = 'Chihuahuan' and (\"north_objects.Vegname\" like '%Riparian%' or \"north_objects.Vegname\" = 'Ramadero')")
DM.CalculateField(layername, "north_objects.VegNum", "[CH_RIP.SYSTEM]", "VB", "")
DM.RemoveJoin(layername, "CH_RIP")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying Chihuahuan riparian. " + elapsed_time(processstart) + "\n")
processstart = time()

# Fix juniper adjacent to EP along edge of Ridge, SW EP Tamaulipan
# Select lulc of 37 which was hand attributed for juniper adjacent to Tamaulipan ridge, riparian buffer attributed to riparian juniper shrubland, uplands to semi-arid juniper shrubland
print "adding juniper to polys adjacent to EP on Ridge, SW EP Tamaulipan...."
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"lulc\" = 37 and \"riparian24\" = 1")
DM.CalculateField(layername, "VegNum", "1405", "VB", "")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"lulc\" = 37 and \"riparian24\" = 0")
DM.CalculateField(layername, "VegNum", "1215", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying juniper near EP in Ridge, SW EP Tamaulipan. " + elapsed_time(processstart) + "\n")
processstart = time()

# Remove juniper shrubland and woodlands from outside range of juniper. Move it to Trans-Pecos Mixed Desert Shrubland
print "removing juniper shrubland outside of range....."
NonJuniper = "Subsets.gdb/NonJuniper_Chihuahuan"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "(\"VegNum\" = 1215 and \"lulc\" = 11) or \"VegNum\" = 1101")
DM.SelectLayerByLocation(layername, "INTERSECT", NonJuniper, "", "SUBSET_SELECTION")
DM.CalculateField(layername, "VegNum", "8306", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed removing juniper outside of range. " + elapsed_time(processstart) + "\n")
processstart = time()

# Remove juniper forest and woodland outside range of juniper
#
# Handled in previous process
#print "removing juniper woodland outside of range...."
#DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 1101")
#DM.SelectLayerByLocation(layername, "INTERSECT", NonJuniper, "", "SUBSET_SELECTION")
#DM.CalculateField(layername, "VegNum", "8306", "VB", "")
#DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")

# Remove live oak forest and woodland outside range of live oak. Move it to Trans-Pecos: Mixed Desert Shrubland
print "removing live oak woodland outside of range...."
bleg = "Subsets.gdb/bleg"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 1102 ")
DM.SelectLayerByLocation(layername, "INTERSECT", NonJuniper, "", "SUBSET_SELECTION")
DM.SelectLayerByLocation(layername, "INTERSECT", bleg, "", "REMOVE_FROM_SELECTION")
DM.CalculateField(layername, "VegNum", "8306", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed removing live oak outside of range. " + elapsed_time(processstart) + "\n")
processstart = time()

# Fix shrubland on Stockton Plateau. Change shrubland on uplands to grassland.
print "changing shrubland on uplands of Stockton Plateau to Grassland...."
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"epa_ecoreg\" =  '24e' and \"lulc\" = 7 and \"slope20\" = 0 and \"cliff\" = 0 and \"riparian24\" = 0 and (\"Ecogroup\" like 'Gravelly, %' or \"Ecogroup\" like 'Limestone%')")
DM.CalculateField(layername, "VegNum", "1207", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed fixing upland shrubs on Stockton Plateau. " + elapsed_time(processstart) + "\n")
processstart = time()

# Correct slope types
print "correcting slope types...."
slopes = "SLPXWALK.dbf"
DM.AddJoin(layername, "VegNum", slopes, "STANDARD", "KEEP_ALL")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"SLPXWALK.SLOPE\" is not null AND \"north_objects.slope20\" =1 AND \"north_objects.cliff\" = 0")
DM.CalculateField(layername, "north_objects.VegNum", "[SLPXWALK.SLOPE]", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
DM.RemoveJoin(layername, "SLPXWALK")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying slopes. " + elapsed_time(processstart) + "\n")
processstart = time()

# Out of range issues Floodplain woodlands
print "correcting out of range floodplain woodlands...."
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 1001 or \"VegNum\" = 1003 or \"VegNum\" = 1002 or \"VegNum\" = 1401 or \"VegNum\" = 1403 or \"VegNum\" = 1402")
DM.SelectLayerByLocation(layername, "INTERSECT", NonJuniper, "", "SUBSET_SELECTION")
DM.SelectLayerByLocation(layername, "INTERSECT", bleg, "", "REMOVE_FROM_SELECTION")
DM.CalculateField(layername, "VegNum", "8704", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed fixing out of range issues in Floodplain woodlands. " + elapsed_time(processstart) + "\n")
processstart = time()

# Out of range issues Floodplain shrublands
print "correcting out of range floodplain shrublands...."
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 1005 or \"VegNum\" = 1405")
DM.SelectLayerByLocation(layername, "INTERSECT", NonJuniper, "", "SUBSET_SELECTION")
DM.SelectLayerByLocation(layername, "INTERSECT", bleg, "", "REMOVE_FROM_SELECTION")
DM.CalculateField(layername, "VegNum", "8706", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed fixing out of range issues in Floodplain shrublands. " + elapsed_time(processstart) + "\n")
processstart = time()

# Change High Plains Mesquite Shrubland to Native Invasive in Chihuahuan Clay Flat
print "changing High Plains Mesquite to native invasive in Chihuahuan...."
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "(\"morap_id\" = 7416 or \"morap_id\" = 75421 or \"morap_id\" = 75435) and \"VegNum\" = 5406")
DM.CalculateField(layername, "VegNum", "9106", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed changing High Plains mesquite to native invasive in Chihuahuan clay flat. " + elapsed_time(processstart) + "\n")
processstart = time()

# Assign cliffs
print "assigning cliffs...."
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"Basin\" = 'Chihuahuan' and \"cliff\" = 1")
DM.CalculateField(layername, "VegNum", "10100", "VB", "")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"Basin\" = 'Edwards Plateau' and \"cliff\" = 1 and (\"lulc\" = 1 or \"lulc\" = 9 or \"lulc\" = 15 or \"lulc\" =21 or \"lulc\" = 23 or \"lulc\" = 25 or \"lulc\" = 27)")
DM.CalculateField(layername, "VegNum", "807", "VB", "")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"Basin\" = 'Edwards Plateau' and \"cliff\" = 1 and (\"lulc\" = 3 or \"lulc\" = 5 or \"lulc\" = 7 or \"lulc\" = 11 or \"lulc\" = 19 or \"lulc\" = 31 or \"lulc\" = 37)")
DM.CalculateField(layername, "VegNum", "806", "VB", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying cliffs. " + elapsed_time(processstart) + "\n")
processstart = time()

# Add saltcedar
print "adding saltcedar...."
DM.AddJoin(layername, "morap_id", slayername, "morap_id", "KEEP_ALL")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"p4soils_working.ecoclassna\" like 'SALTY BOTT%' and ( \"north_objects.lulc\" = 3 or \"north_objects.lulc\" = 5 or \"north_objects.lulc\" = 11 or \"north_objects.lulc\" = 19 or \"north_objects.lulc\" = 31) and \"north_objects.Basin\" = 'Chihuahuan'")
DM.CalculateField(layername, "north_objects.VegNum", "9204", "VB", "")
print "Adding saltcedar process time = " + elapsed_time(processstart)
outf.writelines("Completed applying cliffs. " + elapsed_time(processstart) + "\n")
processstart = time()

# Update VegName using legend in exported dbf table	
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "adding VegName......"
DM.AddJoin(layername, "VegNum", legend, "VEGNUM", "KEEP_ALL")
DM.CalculateField(layername, "north_objects.VegName", "[P4LEG.VEGNAME]", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
DM.RemoveJoin(layername, "P4LEG")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed updating VegName. " + elapsed_time(processstart) + "\n")
processstart = time()

# Dissolve on VegNum/VegName to north_dslv
print "dissolving on Vegnum/VegName..."
dslv = "p4_objects_working.gdb/north_dslv"
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
outf.writelines("\nFinished. " + elapsed_time(starttime) + "\n")
outf.close()

