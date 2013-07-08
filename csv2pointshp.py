import(arcpy)
import(os)

sr = arcpy.SpatialReference("NAD 1983 UTM ZONE 12N")
csv_input = "qoa.csv"
temp_layer = "output"
arcpy(MakeXYEventLayer_management(csv_input,"utm_n","utm_e", temp_layer, sr)
arcpy.FeatureClassToShapefile_conversion(temp_layer)
arcpy.Delete_management(temp_layer)