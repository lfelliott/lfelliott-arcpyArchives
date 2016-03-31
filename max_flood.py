import arcpy
from arcpy.sa import *
from arcpy import management as DM
import os

# DEM raster file
dem = "loess_fill.img"
# Dam layer with elevation of bottom of dam, elevation of top of dam, and id.
# Currently fields are called id (integer), top (double), bottom (double), dam_id (string 80)
# It really only needs one of the id fields. But code below will have to be changed to reflect which type will be used.
dam_shapefile = 'dams.shp'
# Feature class where max storage polygons will be placed. This feature class needs to have
# same attribute structure as shapefile appended to it below. raster to poly then add text dam_id field.
max_stor = 'MaxStorage.gdb/max_storage'

max_elev = 400 # maximum elevation in DEM
arcpy.env.workspace = os.getcwd()
class LicenseError(Exception):
    pass
try:
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        print "Spatial Analyst license is AVAILABLE"
    else:
        # raise a custom exception
        #
        raise LicenseError
except LicenseError:
    print "Spatial Analyst license is unavailable"
except:
    print arcpy.GetMessages(2)

damlayer = 'dam_layer'
DM.MakeFeatureLayer(dam_shapefile, damlayer)
rows = arcpy.SearchCursor(dam_shapefile)
out_shp_name = 'temp_wshd.shp'
templayer = 'temp_layer'
for row in rows:
# Need to change quoted text in next 4 lines to reflect field names in dams feature class
# Currently fields are called id (integer), top (double), bottom (double), dam_id (string 80)
	bottom = row.getValue("bottom")
	id = row.getValue("id")
	top = row.getValue("top")
	dam_str = row.getValue("dam_id")
	dam_idstr = "\"%s\"" % dam_str
	print "Getting poly for " + dam_idstr
#	Also could use a constant integer for id, since id string is added to shapefile below. Only makes sense to use
#   integer id from dams shapefile if it works as a gridcode.
	rng = [[0, bottom, "NoData"],[bottom,top, id], [top, max_elev, "NoData"]]
	out_recls = Reclassify(dem, "Value", RemapRange(rng), "NoData")
	arcpy.RasterToPolygon_conversion(out_recls, out_shp_name, "NO_SIMPLIFY", "VALUE")
	DM.MakeFeatureLayer(out_shp_name, templayer)
#	Should use string id here.
	selectstr = "\"dam_id\" = '%s'" % dam_str
#	selectstr = '\"Id\" = %s' % id
	DM.SelectLayerByAttribute(damlayer, "NEW_SELECTION", selectstr)
	DM.SelectLayerByLocation(templayer, 'intersect', damlayer)
	count = int(DM.GetCount(templayer).getOutput(0))
	if count == 1:
		DM.AddField(templayer, "dam_id", "TEXT", "","","80","","", "","")
		DM.CalculateField(templayer, "dam_id", dam_idstr, "VB", "")
		print "     Adding poly to feature class"
		DM.Append(templayer, max_stor, "TEST", "","")
#   Or you could save it as a separate file and delete all but the relevant feature.
#	DM.SelectLayerByAttribute(templayer, "SWITCH_SELECTION")
#	count = int(DM.GetCount(templayer).getOutput(0))
#	if count > 0:
#		DM.DeleteFeatures(templayer)
#		print "Deleted"
	DM.Delete(templayer)
	DM.Delete(out_shp_name)
