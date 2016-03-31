#Batch calculate area
import os
import arcpy
from arcpy import management as DM

arcpy.env.workspace = "f:/projects/ewg/Nugget40_IL/"
fcs = arcpy.ListFeatureClasses("*")
for fc in (fcs):
	print fc
#	DM.AddField(fc, "Shape_Area", "DOUBLE")
	DM.CalculateField(fc, "Shape_Area", "!shape.area@squaremeters!", "PYTHON_9.3", "#")
	
	
	