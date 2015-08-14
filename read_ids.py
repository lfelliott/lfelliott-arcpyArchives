import arcpy
from arcpy import management as DM
arcpy.env.workspace = "F:/NPS_VegMap/PAIS/GIS/New/PAIS_Veg_Final.gdb"
tile_fc = "tiles"
tiles = "tiles"
id_fldnm = "ID"
DM.MakeFeatureLayer(tile_fc, tiles)
rows = arcpy.SearchCursor(tile_fc, "", "", id_fldnm)
ids = []
for row in rows:
	ids.append(row.ID)
for id in ids:
	sqlstr = "ID = %d" % (id)
	print sqlstr
print len(ids)