# Reclass skeleton
import arcpy
from arcpy.sa import *
from arcpy import management as DM
import os

# DEM raster file
dem = "loess_fill.img"
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
	
rng = [[0, bottom, "NoData"],[bottom,top, id], [top, max_elev, "NoData"]]
out_recls = Reclassify(dem, "Value", RemapRange(rng), "NoData")
values = [[1, "NoData"], [2, id]]
out_recls = Reclassify(out_recls, "Value", RemapValue(values))
out_recls.save("reclassout.tif")