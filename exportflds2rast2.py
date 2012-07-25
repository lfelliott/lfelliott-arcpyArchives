# ---------------------------------------------------------------------------
# export.py
# Created on: 2012-07-25 09:35:54.00000
# export multiple fields within poly to raster python script
# Ronnie Lee

import arcpy
env.workspace = sys.path[0]
polygons = "tm_objects_3.shp"
fieldList = arcpy.ListFields(polygons)
for field in fieldList:
    print "working on " + field.name + "\a"
    if ((field.name != "FID") & (field.name != "Shape")):
        tempEnvironment0 = arcpy.env.snapRaster        
        arcpy.env.snapRaster = "G:\\2011_MDC_Elk\\final\\Elk_Final to deliver\\DATA\\Elk_Habitat_LULC_30m.img"         
        arcpy.PolygonToRaster_conversion(polygons, field.name, field.name, "CELL_CENTER", "NONE", "30")		
print "complete \a\a\a\a\a\a\a\a\a\a\a"