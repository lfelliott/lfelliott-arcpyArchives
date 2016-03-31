import arcpy
from arcpy import management as DM
import os

outfile = open("padreshape_fields.txt", "a")
#arcpy.env.workspace = "M:/Padre"
#in_workspace = r"M:/Padre"
in_workspace = 'F:/NPS_Vegmap/PAIS/GIS'
feature_classes = []
# fcs = arcpy.ListFeatureClasses("*")
for dirpath, dirnames, filenames in arcpy.da.Walk(in_workspace, datatype="FeatureClass", type="Polygon"):
	if "Rasters" in dirnames:
		dirnames.remove("Rasters")
	for filename in filenames:
		feature_classes.append(os.path.join(dirpath, filename))
#feature_classes = arcpy.ListFeatureClasses(feature_type = "Polygon")
for fc in feature_classes:
	desc = arcpy.Describe(fc)
	fields = desc.fields
	
#	fieldnames = [f.name for f in arcpy.ListFields(fc)]
	for field in fields:
		outstr = "\"%s\", \"%s\"\n" % (fc, field.name)
#		outfile.write(outstr)
		if (field.name == 'Confirmed'):
			print fc
