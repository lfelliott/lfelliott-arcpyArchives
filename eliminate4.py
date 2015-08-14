from time import time
from string import zfill
from datetime import date
import arcpy
from arcpy import management as DM
arcpy.env.workspace = "F:/NPS_VegMap/PAIS/GIS/New/PAIS_Veg_Final.gdb"

output_fc = "pais_veg_smthtopo_elm15e"
preliminary_fc = "pais_veg_smthtopo_elm15d"
tile_fc = "tiles"
tiles = "tiles"
DM.MakeFeatureLayer(tile_fc, tiles)

# Get values of attribute ID in tiles
rows = arcpy.SearchCursor(tile_fc, "", "", "ID")
ids = []
for row in rows:
	ids.append(row.ID)

def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

i = 0
#if (i == 0):
DM.CopyFeatures(preliminary_fc, "pais_temp1")	
starttime = time()
for id in ids:
	i += 1
	processtime = time()
	sqlstr = "ID = %d" % (id)
	in_fc = "pais_temp1"
	elim_in = "input"
	elim_out = "pais_temp2"
	DM.MakeFeatureLayer(in_fc, elim_in)
#	DM.SelectLayerByAttribute(elim_in, "NEW_SELECTION", "(Class = 'X5' or Class = 'X6' or Class = 'X15') and shape_area < 2000")
	DM.SelectLayerByAttribute(elim_in, "NEW_SELECTION", "(Class = 'X4' or Class = 'X5' or Class = 'X6' or Class = 'X12' or Class = 'X13' or Class = 'X16' or Class = 'X17' or Class = 'X15') and shape_area < 2500")
	print sqlstr
	DM.SelectLayerByAttribute(tiles, "NEW_SELECTION", sqlstr)
	DM.SelectLayerByLocation(elim_in, "INTERSECT", tiles, "", "SUBSET_SELECTION")
	DM.Eliminate(elim_in, elim_out, "LENGTH", "", "")
	DM.Delete(elim_in)
	DM.Delete(in_fc)
	DM.CopyFeatures(elim_out, "pais_temp1")
	DM.Delete(elim_out)
	print elapsed_time(processtime)
	print "Done with %d of %d" % (i, len(ids))
	
print elapsed_time(starttime)
DM.CopyFeatures("pais_temp1", output_fc)
DM.Delete("pais_temp1")

