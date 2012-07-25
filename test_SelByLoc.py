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
starttime = time()
objects = "p4_objects_working.gdb/south_objects"
layername = "south_layer"
blegobjs = "Subsets.gdb/bleg"
bleg = "bleg_layer"
DM.MakeFeatureLayer(objects, layername)
DM.MakeFeatureLayer(blegobjs, bleg)
processstart = time()


# Add Live Oak types to sandy and floodplain areas of the South Texas Plains
print "add live oak types to sandy/floodplain of South Texas"
DM.SelectLayerByAttribute(bleg, "NEW_SELECTION", "\"Type\" = 'Live Oak'")
DM.SelectLayerByAttribute(layername, "NEW_SELECTION", "\"VegNum\" = 99999")
DM.SelectLayerByLocation(layername, "INTERSECT", bleg, "", "SUBSET_SELECTION")
DM.CalculateField(layername, "VegNum", "99998", "VB", "")
print "process time = " + elapsed_time(processstart)

