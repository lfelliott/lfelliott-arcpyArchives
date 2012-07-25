# ---------------------------------------------------------------------------
# subst.py
# Created on: 2011-07-05 10:58:52.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# Local variables:
south_objects = "south_objects"
bleg = "bleg"
south_objects__6_ = "south_objects"
bleg__2_ = "bleg"
south_objects__4_ = "south_objects"
south_objects__2_ = "south_objects"

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management(south_objects, "NEW_SELECTION", "\"VegName\" LIKE '%Live Oak%' ")

# Process: Select Layer By Attribute (2)
arcpy.SelectLayerByAttribute_management(bleg, "NEW_SELECTION", "\"Type\" = 'Live Oak'")

# Process: Select Layer By Location
arcpy.SelectLayerByLocation_management(south_objects__6_, "INTERSECT", bleg__2_, "", "REMOVE_FROM_SELECTION")

# Process: Calculate Field
arcpy.CalculateField_management(south_objects__4_, "VegNum", "7103", "VB", "")

# Process: Calculate Field (2)
arcpy.CalculateField_management(south_objects__2_, "VegName", "\"South Texas: Sandy Mesquite / Evergreen Woodland\"", "VB", "")

