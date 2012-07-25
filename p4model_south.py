import arcpy
from arcpy import management as DM
from time import time
from string import zfill
from datetime import date
arcpy.env.workspace = "C:/WorkSpace/Phase4"

def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

# Apply models from key in separate dbf for each landcover
suffixes = ["01","03","05","07","09","11","13","15","19","21","23","25","27","31"]
covers = [1,3,5,7,9,11,13,15,19,21,23,25,27,31]
starttime = time()
objects = "p4_objects_working.gdb/south_objects"
blegobjs = "Subsets.gdb/bleg"
bleg = "bleg_layer"
layername = "south_layer"
leader = "QKEY%s.dbf"
outf = open("c:/workspace/phase4/modellog.txt", "a")
outf.writelines("\n" + str(date.today()) + " --South--\n")
DM.MakeFeatureLayer(objects, layername)
DM.MakeFeatureLayer(blegobjs, bleg)
processstart = time()
for i in range(len(suffixes)):
	qname = leader % suffixes[i]
	qsystem = "[QKEY%s.SYSTEM]" % suffixes[i]
	qrmjoin = "QKEY%s" % suffixes[i]
	landcover = "\"south_objects.lulc\" = %s" % covers[i]
	print qname, qsystem, qrmjoin, landcover
	print "joining....."
	DM.AddJoin(layername, "Ecogroup", qname, "ECOGROUP", "KEEP_ALL")
	print "selecting....."
	DM.SelectLayerByAttribute(layername, "NEW_SELECTION", landcover)
	print "calculating....."
	DM.CalculateField(layername, "south_objects.VegNum", qsystem, "VB", "")
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
DM.CalculateField(layername, "south_objects.VegName", "[P4LEG.VEGNAME]", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
DM.RemoveJoin(layername, "P4LEG")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed updating VegName. " + elapsed_time(processstart) + "\n")
processstart = time()

# Apply riparian models to NHD24 buffers
# Selecting objects within Coastal Bend basin within riparian buffer or having riparian or ramadero soils
CB_RIP = "CB_RIP.DBF"
print "applying CB Riparian...."
DM.AddJoin(layername, "lulc", CB_RIP, "COVERTYPE", "KEEP_ALL")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"south_objects.Basin\" = 'Coastal Bend' and ( \"south_objects.riparian24\" = 1  or \"south_objects.Vegname\" like '%Riparian%' or \"south_objects.Vegname\" = 'Ramadero') and \"south_objects.Ecogroup\" not like '%Bottomland%'")
DM.CalculateField(layername, "south_objects.VegNum", "[CB_RIP.SYSTEM]", "VB", "")
DM.RemoveJoin(layername, "CB_RIP")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying Coastal Bend riparian. " + elapsed_time(processstart) + "\n")
processstart = time()

# Selecting objects within Tamaulipan basin within riparian buffer or having riparian or ramadero soils
TAM_RIP = "TAM_RIP.DBF"
print "applying TAM Riparian...."
DM.AddJoin(layername, "lulc", TAM_RIP, "COVERTYPE", "KEEP_ALL")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"south_objects.Basin\" = 'Tamaulipan' and ( \"south_objects.riparian24\" = 1  or \"south_objects.Vegname\" like '%Riparian%' or \"south_objects.Vegname\" = 'Ramadero')\"south_objects.Ecogroup\" not like '%Bottomland%'")
DM.CalculateField(layername, "south_objects.VegNum", "[TAM_RIP.SYSTEM]", "VB", "")
DM.RemoveJoin(layername, "TAM_RIP")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed applying Tamaulipan riparian. " + elapsed_time(processstart) + "\n")
processstart = time()

# Change sandsheet live oak to Mesquite/Evergreen outside of range of Live Oak.
print "removing sandsheet live oak outside of range"
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegName\" LIKE '%Live Oak%' ")
DM.SelectLayerByAttribute(bleg, "NEW_SELECTION", "\"Type\" = 'Live Oak'")
DM.SelectLayerByLocation(layername, "INTERSECT", bleg, "", "REMOVE_FROM_SELECTION")
DM.CalculateField(layername, "VegNum", "7103", "VB", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed removing live oak outside of range. " + elapsed_time(processstart) + "\n")
processstart = time()

# Add Live Oak types to sandy and floodplain areas of the South Texas Plains
print "add live oak types to sandy/floodplain of South Texas"
DM.SelectLayerByAttribute(bleg, "NEW_SELECTION", "\"Type\" = 'Live Oak'")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 7103 and \"lulc\" = 3 and \"Ecogroup\" <> 'Sandy, Sandsheet'")
DM.SelectLayerByLocation(layername, "INTERSECT", bleg, "", "SUBSET_SELECTION")
DM.CalculateField(layername, "VegNum", "7102", "VB", "")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 7402 and \"lulc\" = 3")
DM.SelectLayerByLocation(layername, "INTERSECT", bleg, "", "SUBSET_SELECTION")
DM.CalculateField(layername, "VegNum", "7412", "VB", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed live oak corrections. " + elapsed_time(processstart) + "\n")
processstart = time()

# Add Caliche Grasslands
print "add caliche grasslands"
calicheclass = "Subsets.gdb/CalicheGrasslands"
calichegrasslands = "caliche_layer"
DM.MakeFeatureLayer(calicheclass, calichegrasslands)
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "(\"Ecogroup\" like 'Shallow Sandy%' or \"Ecogroup\" = 'Sandy, Sandsheet') and \"lulc\" = 15")
DM.SelectLayerByLocation(layername, "INTERSECT", calichegrasslands, "", "SUBSET_SELECTION")
DM.CalculateField(layername, "VegNum", "6707", "VB", "")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed caliche grassland additions. " + elapsed_time(processstart) + "\n")
processstart = time()


# Update VegName using legend in exported dbf table	
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
print "adding VegName......"
DM.AddJoin(layername, "VegNum", legend, "VEGNUM", "KEEP_ALL")
DM.CalculateField(layername, "south_objects.VegName", "[P4LEG.VEGNAME]", "VB", "")
DM.SelectLayerByAttribute(layername, "CLEAR_SELECTION", "")
DM.RemoveJoin(layername, "P4LEG")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed updating VegName. " + elapsed_time(processstart) + "\n")
processstart = time()

# Dissolve on VegNum/VegName to north_dslv
print "dissolving on Vegnum/VegName..."
dslv = "p4_objects_working.gdb/south_dslv"
DM.Dissolve(objects, dslv, "VegNum;VegName", "", "MULTI_PART", "DISSOLVE_LINES")
print "process time = " + elapsed_time(processstart)
outf.writelines("Completed dissolve. " + elapsed_time(processstart))
processstart = time()

# Repair geometry
print "Starting repair geometry......"
DM.RepairGeometry(dslv, "DELETE_NULL")
print "Repair geometry process time = " + elapsed_time(processstart)
outf.writelines("Completed repair geometry. " + elapsed_time(processstart) + "\n")

print "Finished - Elapsed Time = " + elapsed_time(starttime)
outf.writelines("\nFinished. " + elapsed_time(starttime) + "\n")
outf.close()